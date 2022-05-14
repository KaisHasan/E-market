from django.forms import Form, RadioSelect
from django.forms import ChoiceField
from .models import Product
from django import forms


class SearchForm(Form):
    template_name = 'products/search_form.html'


class CompareForm(Form):
    template_name = 'products/compare_form.html'

    CHOICES = list(('', ''))
    product = ChoiceField(choices=CHOICES, label='Compare with:')

    def __init__(self, view_context, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].choices = list(Product.objects.all().values_list('id', 'name'))
        self.view_context = view_context
    
    def update_view_context(self, context):
        self.view_context.update(context)

    def get_context(self, **kwargs):
        context = super().get_context(**kwargs)
        context.update(self.view_context)
        return context


class SortForm(Form):
    template_name = 'products/sort_by_form.html'
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
