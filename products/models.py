from email.policy import default
from django.urls import reverse
from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.db.models import Avg

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    categories = models.ManyToManyField(
        Category,
        related_name='products',
        blank=True,
        null=True
    )

    def get_rating(self):
        avg_stars = self.reviews.aggregate(
            avg_stars=Avg('stars', default=None)
        )['avg_stars']
        return avg_stars
    
    def get_num_reviews(self):
        return self.reviews.count()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})


class StarredProducts(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='+'
    )

    def __str__(self):
        return f'User: {self.user} have starred {self.product}.'
