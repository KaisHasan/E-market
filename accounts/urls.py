from django.urls import path
from .views import ResetView, AccountInfoView


urlpatterns = [
    path('reset/', ResetView.as_view(), name='reset'),
    path('info/', AccountInfoView.as_view(), name='account-info')
]
