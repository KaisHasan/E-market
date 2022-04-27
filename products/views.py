from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from .models import Product
from django.db.models import Q
# Create your views here.
class ProductList(ListView):
    template_name = "products\product_list.html"
    model = Product
    context_object_name = 'product_list'


class ProductDetail(DetailView):
    template_name = "products\product_detail.html"
    model = Product


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


class CategoryProducts(ListView):
    template_name = "products\product_list.html"
    model = Product
    context_object_name = 'product_list'
    def get_queryset(self):
        query = self.kwargs['category_name']
        print(query)
        return Product.objects.filter(
            category__name=query
        )
