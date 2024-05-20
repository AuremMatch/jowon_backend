from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RatingViewSet



urlpatterns = [
    path('', RatingViewSet.as_view({'get': 'list', 'post': 'create'}), name='conversation-list'),
]