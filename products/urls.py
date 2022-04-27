from django.urls import path
from .views import ProductList, SearchProducts, CategoryProducts, ProductDetail

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('search_results/', SearchProducts.as_view(), name='search_results'),
    path('category_products/<str:category_name>', CategoryProducts.as_view(), name='category_products'),
    path('product_detail/<uuid:pk>/', ProductDetail.as_view(), name='product_detail')
]
