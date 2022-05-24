from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum

# Create your models here.
class CustomUser(AbstractUser):
    money = models.PositiveIntegerField(
        default=1000
    )
    def get_num_of_items_in_cart(self):
        num = self.orders.filter(
            archived=False
        ).aggregate(
            n=Sum('num_items', default=0)
        )['n']
        if num > 9:
            num = '+9'
        return num
    
    def reset(self):
        self.cart.reset()
