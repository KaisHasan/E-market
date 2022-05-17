from itertools import product
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from products.models import Product


# Create your models here.
class Review(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    comment = models.TextField(max_length=1000, blank=True, default='')

    CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    stars = models.PositiveSmallIntegerField(choices=CHOICES)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        null=True
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        null=True
    )

    
    def __str__(self):
        return f'user: {self.user} gives this product {self.stars} stars'

