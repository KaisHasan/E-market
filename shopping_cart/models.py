from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import F
from products.models import Product
from django.db.models import Sum
from django.contrib import messages


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        related_name='cart',
        on_delete=models.CASCADE
    )
    def add_to_cart(self, product_id, num_of_items):
        product = get_object_or_404(Product, pk=product_id)
        order_price = product.price * num_of_items
        tot_price = order_price + self.get_tot_price()
        if tot_price > self.user.money:
            # TODO: Show an error or something
            return False
        order, created = Order.objects.get_or_create(
            user=self.user,
            product=product,
            cart=self,
            archived=False
        )
        if created:
            num_of_items -= 1

        order.num_items = F('num_items') + num_of_items
        order.save()
        return True
    
    def get_tot_price(self):
        return self.orders.all().filter(
            archived=False
        ).annotate(
            sum_price=F('product__price')*F('num_items')
        ).aggregate(
            tot_price=Sum('sum_price', default=0)
        )['tot_price']

    def buy(self):
        tot_price = self.get_tot_price()
        self.user.money = F('money') - tot_price
        self.user.save()
        self.orders.all().update(archived=True)

    def reset(self):
        take_back_money = self.orders.filter(
            archived=True
        ).annotate(
            sum_price=F('product__price')*F('num_items')
        ).aggregate(
            tot_price=Sum('sum_price', default=0)
        )['tot_price']
        self.user.money = F('money') + take_back_money
        self.user.save()
        self.orders.all().delete()



    def remove_from_cart(self, product_id):
        product = get_object_or_404(Product, pk=product_id)
        order = Order.objects.get(user=self.user, product=product, cart=self)
        if order.num_items == 1:
            order.delete()
        else:
            order.num_items = F('num_items') - 1
            order.save()

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
    archived = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f'{self.user.username} ordered {self.num_items} items of {self.product.name}'
    

