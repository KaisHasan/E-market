from ast import Add
from mimetypes import init
from django.views.generic import DetailView, ListView
from .models import Category, Product
from django.views import View
from django.shortcuts import get_object_or_404
from .models import StarredProducts
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser
from reviews.models import Review
from .forms import CompareForm, SortForm, SearchForm
from .forms import AddToCartForm
from django.db.models import Avg
from dal import autocomplete


# Create your views here.
class ProductList(ListView):

    template_name = "products/product_list.html"
    model = Product
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Categories
        categories_objects = Category.objects.all()
        categories = []
        for category in categories_objects:
            name = category.name
            num = category.products.all().count()
            categories.append((name, num))

        context['categories'] = categories

        # Forms
        desc_asc, sort_by, q = None, None, None
        if 'desc_asc' in self.request.GET:
            desc_asc = self.request.GET.get('desc_asc')
        if 'sort_by' in self.request.GET:
            sort_by = self.request.GET.get('sort_by')
        if 'q' in self.request.GET:
            q = self.request.GET.get('q')
        # strs = ['desc_asc', 'sort_by', 'q']
        # for v, n in zip([desc_asc, sort_by, q], strs):
        #     if n in self.request.GET:
        #         v= self.request.GET.get(n)

        print(desc_asc)
        sort_form = SortForm(
            initial={
                'sort_by':sort_by,
                'desc_asc':desc_asc
            }
        )
        search_form = SearchForm(
            initial={
                'q':q
            }
        )
        sort_form.set_search_form(search_form)
        search_form.set_sort_form(sort_form)
        context['sort_by_form'] = sort_form
        context['search_form'] = search_form

        # User specific
        if isinstance(self.request.user, AnonymousUser):
            return context 
        favorites = StarredProducts.objects.filter(
            user=self.request.user
        ).values_list('product')
        favorites = [product[0] for product in list(favorites)]
        context['starred_products'] = favorites
        return context

    def get_ordering(self):
        try:
            ordering = self.request.GET.get('sort_by')
            desc_asc = self.request.GET.get('desc_asc')
            if ordering not in ['name', 'price']:
                raise KeyError
            if desc_asc == 'desc':
                ordering = '-' + ordering
            return ordering
        except KeyError:
            return super().get_ordering()


    def get_queryset(self):
        query = super().get_queryset()

        # Search filter
        if 'q' in self.request.GET:
            q = self.request.GET.get('q')
            query = query.filter(
                name__icontains=q
            )

        # Order filter
        result, query = self.order_by_rating(query)

        return query


    def order_by_rating(self, cur_queryset):
        """Return (result, query)
        result is True when order applied,
            and query will be the ordered queryset
        resutl is False when order did not applied,
            and query will be the passed one
        """
        try:
            ordering = self.request.GET.get('sort_by')
            desc_asc = self.request.GET.get('desc_asc')
            if ordering != 'rating':
                raise KeyError
            ordered_queryset = sorted(
                cur_queryset,
                key=lambda p: p.get_rating() if p.get_rating() is not None else 0,
                reverse=(desc_asc=='desc')
            )
            return True, ordered_queryset
        except KeyError:
            return False, cur_queryset
        


class ProductDetail(DetailView):

    template_name = "products/product_detail.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add to cart
        context['add_to_cart_form'] = AddToCartForm(
            initial={
                'num_of_items': 1
            }
        )

        # Reviews related
        reviews = Review.objects.filter(
            product=self.kwargs['pk']
        )
        context['reviews'] = reviews
        context.update(
            reviews.aggregate(
                avg_stars=Avg('stars', default=0)
            )
        )
        context['num_reviews'] = reviews.count()

        # CompareForm context
        if 'product' in self.request.GET:
            other_product_key = self.request.GET.get('product')
        else:
            other_product_key = self.kwargs['pk']
        context['compare_form'] = CompareForm(
            initial={
                'product':other_product_key
            },
            view_context = {
                'product_pk': self.kwargs['pk'],
                'show_compare': False
            }
        )

        # User specific context
        if isinstance(self.request.user, AnonymousUser):
            return context      
        favorites = StarredProducts.objects.filter(
            user=self.request.user
        ).values_list('product')
        favorites = [product[0] for product in list(favorites)]
        context['starred_products'] = favorites

        if Review.objects.filter(user=self.request.user, product=self.kwargs['pk']):
            context['user_not_posted_review'] = 0
        else:
            context['user_not_posted_review'] = 1
        
        return context


class CategoryProducts(ProductList):

    def get_queryset(self):
        query = self.kwargs['category_name']
        print(query)
        category = Category.objects.filter(
            name=query
        ).get()
        return category.products.all()
        


class StarredProductsList(LoginRequiredMixin, ListView):
    template_name = "products/starred_product_list.html"
    model = StarredProducts
    context_object_name = 'starred_product_list'

    def get_queryset(self):
        return StarredProducts.objects.filter(user=self.request.user)


class StarUnStarProduct(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        user = request.user
        try:
            starred_product = StarredProducts.objects.get(user=user, product=product)
            starred_product.delete()
        except StarredProducts.DoesNotExist:
            starred_product = StarredProducts.objects.create(user=user, product=product)
        next = request.GET.get('next')
        return HttpResponseRedirect(next)


class CompareView(ProductDetail):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['compare_form'].update_view_context(
            {
                'show_compare': True,
                'first_item': Product.objects.get(
                    id=self.kwargs['pk']
                ),
                'second_item': Product.objects.get(
                    id=self.request.GET.get('product')
                )
            }
        )
        return context


class ProductAutoComplete(autocomplete.Select2ListView):

    def get_list(self):
        products_names = list(
            Product.objects.all().values_list('id', 'name')
        )
        print('hi')
        return products_names

