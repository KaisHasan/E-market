from django.urls import path
from .views import CartItemsList, AddItemView, RemoveItemView
urlpatterns = [
    path('add_item/<uuid:pk>', AddItemView.as_view(), name='add_item'),
    path('remove_item/<uuid:pk>', RemoveItemView.as_view(), name='remove_item'),
    path('', CartItemsList.as_view(), name='cart_items'),
]
