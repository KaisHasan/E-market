from django.forms import Form, RadioSelect
from django.forms import ChoiceField
from .models import Product
from django import forms
from dal import autocomplete


class SearchForm(Form):
    template_name = 'products/search_form.html'

    q = forms.CharField(max_length=20, label='Search in products')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sort_form = None
        self.fields['q'].widget.attrs['class'] = 'search-text form-control mr-sm-2'
        self.fields['q'].widget.attrs['aria-label'] = 'Search through site products'


    
    def set_sort_form(self, sort_form):
        self.sort_form = sort_form

    def get_context(self, **kwargs):
        context = super().get_context()
        context['sort_form'] = self.sort_form
        return context




class CompareForm(Form):

    template_name = 'products/compare_form.html'

    CHOICES = list(('', ''))
    product = autocomplete.Select2ListChoiceField(
        choice_list=CHOICES, label='Compare with:',
        widget=autocomplete.ListSelect2(url='product-autocomplete')
    )

    def __init__(self, view_context, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].choices = list(
            Product.objects.all().values_list('id', 'name')
        )
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
        ('price', 'Price'),
        ('rating', 'Rating')
    ]
    sort_by = ChoiceField(choices=CHOICES1, label='', widget=forms.RadioSelect)
    CHOICES2 = [
        ('desc', 'Desc.'), ('asc', 'Asc.')
    ]
    desc_asc = ChoiceField(choices=CHOICES2,label='', widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(SortForm, self).__init__(*args, **kwargs)
        self.search_form = None
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-inline'

    def set_search_form(self, search_form):
        self.search_form = search_form

    def get_context(self, **kwargs):
        context = super().get_context()
        context['search_form'] = self.search_form
        return context

