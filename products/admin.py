from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Category, Product
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)