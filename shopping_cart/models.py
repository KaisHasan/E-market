from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import F
from products.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        related_name='cart',
        on_delete=models.CASCADE
    )
    def add_to_cart(self, product_id):
        product = get_object_or_404(Product, pk=product_id)
        order, created = Order.objects.get_or_create(
            user=self.user,
            product=product,
            cart=self
        )
        if not created:
            order.num_items = F('num_items') + 1
            order.save()


    def remove_from_cart(self, product_id):
        product = get_object_or_404(Product, pk=product_id)
        order = Order.objects.get(user=self.user, product=product, cart=self)
        order.delete()

    def __str__(self):
        return f'Cart for {self.user.username}'


class Order(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='orders'
    )
    product = models.ForeignKey(
        Product,
        related_name='orders',
        on_delete=models.CASCADE
    )
    num_items = models.PositiveSmallIntegerField(
        'number of items', default=1
    )
    cart = models.ForeignKey(
        Cart,
        related_name='orders',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.user.username} ordered {self.num_items} items of {self.product.name}'
    

