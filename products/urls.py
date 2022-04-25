from django.urls import path
from .views import ProductList, SearchProducts

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('search_results/', SearchProducts.as_view(), name='search_results')
]
