# Generated by Django 4.0.4 on 2022-05-11 09:03

from django.db import migrations

import json

def populate_data(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    Category = apps.get_model('products', 'Category')
    Category.objects.create(name='Books')
    Category.objects.create(name='Video games')
    with open(r'././data.json', 'r') as f:
        data = json.load(f)
    data = [tuple(x.values()) for x in data['products']]
    for name, price, categories in data:
        categories_q = Category.objects.filter(
            name__in=categories
        )
        product = Product.objects.create(
            name=name,
            price=price,
        )
        product.categories.set(categories_q)
        product.save()

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_data)
    ]
