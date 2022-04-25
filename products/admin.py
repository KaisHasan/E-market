from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Category, Product
# Register your models here.
class ProductInLine(admin.TabularInline):
    model = Product


class CategoryAdmin(ModelAdmin):
    inlines = [
        ProductInLine,
    ]

admin.site.register(Product)
admin.site.register(Category, CategoryAdmin)