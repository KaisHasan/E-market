from django.urls import path, re_path
from .views import ProductList, CategoryProducts, ProductDetail
# from .views import SearchProducts
from .views import StarredProductsList, StarUnStarProduct,CompareView
from products.views import ProductAutoComplete



urlpatterns = [
    re_path(
        r'^product-autocomplete/$',
        ProductAutoComplete.as_view(),
        name='product-autocomplete'
    ),
    path('', ProductList.as_view(), name='product_list'),
    # path('search_results/', SearchProducts.as_view(), name='search_results'),
    path('category_products/<str:category_name>', CategoryProducts.as_view(), name='category_products'),
    path('product_detail/<uuid:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('favorites/star_unstar/<uuid:pk>', StarUnStarProduct.as_view(), name='star_unstar'),
    path('favorites/', StarredProductsList.as_view(), name='favorites'),
    path('compare/<uuid:pk>/', CompareView.as_view(), name='compare'),
    
]
