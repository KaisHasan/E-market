from django.urls import path
from .views import HomePageView
from .views import ContactUsView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact_us/', ContactUsView.as_view(), name='contact-us')
]
