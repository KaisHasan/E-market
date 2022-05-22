from pipes import Template
import django
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import Cart
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
# Create your views here.

class CartItemsList(TemplateView):
    template_name = "shopping_cart/cart_items.html"


class AddItemView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        if request.method == 'POST':
            num_of_items = int(request.POST.get('num_of_items'))
            cart.add_to_cart(kwargs['pk'], num_of_items)
            return redirect(reverse('product_detail', kwargs={'pk':kwargs['pk']}))

class RemoveItemView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.remove_from_cart(kwargs['pk'])
        return redirect(reverse('cart_items'))