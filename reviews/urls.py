from django.urls import path
from .views import CreateReviewView, DeleteReviewView


urlpatterns = [
    path('review/create/<uuid:pk>/', CreateReviewView.as_view(), name='add_review'),
    path('review/delete/<uuid:pk>/', DeleteReviewView.as_view(), name='delete_review'),
]
