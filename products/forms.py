from django.forms import Form
from django.forms import ChoiceField
from .models import Product


class CompareForm(Form):
    CHOICES = list(Product.objects.all().values_list('id', 'name'))
    product = ChoiceField(choices=CHOICES, label='Compare with:')
