from itertools import product
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from .models import Category, Product
from django.db.models import Q
from django.db.models import F
from django.views import View
from django.shortcuts import get_object_or_404
from .models import StarredProducts
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser
from reviews.models import Review


# Create your views here.
class ProductList(ListView):

    template_name = "products\product_list.html"
    model = Product
    context_object_name = 'product_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if isinstance(self.request.user, AnonymousUser):
            return context 
        favorites = StarredProducts.objects.filter(
            user=self.request.user
        ).values_list('product')
        favorites = [product[0] for product in list(favorites)]
        context['starred_products'] = favorites
        return context


class ProductDetail(DetailView):

    template_name = "products\product_detail.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(
            product=self.kwargs['pk']
        )
        if isinstance(self.request.user, AnonymousUser):
            return context      
        favorites = StarredProducts.objects.filter(
            user=self.request.user
        ).values_list('product')
        favorites = [product[0] for product in list(favorites)]
        context['starred_products'] = favorites
        
        return context


class SearchProducts(ListView):

    template_name = "products\product_list.html"
    model = Product
    context_object_name = 'product_list'
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(name__icontains=query)
            |Q(category__name__icontains=query)
        )


class CategoryProducts(ProductList):

    def get_queryset(self):
        query = self.kwargs['category_name']
        print(query)
        category = Category.objects.filter(
            name=query
        ).get()
        return category.products.all()
        


class StarredProductsList(LoginRequiredMixin, ListView):
    template_name = "products\starred_product_list.html"
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
