from django.urls import reverse
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product", kwargs={"pk": self.pk})
    
