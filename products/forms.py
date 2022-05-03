from django.forms import Form, RadioSelect
from django.forms import ChoiceField
from .models import Product
from django import forms

class CompareForm(Form):
    CHOICES = list(Product.objects.all().values_list('id', 'name'))
    product = ChoiceField(choices=CHOICES, label='Compare with:')


class SortForm(Form):
    CHOICES1 = [
        ('name', 'Name'),
        ('price', 'Price')
    ]
    sort_by = ChoiceField(choices=CHOICES1, label='', widget=forms.RadioSelect)
    CHOICES2 = [
        ('desc', 'Desc.'), ('asc', 'Asc.')
    ]
    desc_asc = ChoiceField(choices=CHOICES2,label='', widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(SortForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-inline'
