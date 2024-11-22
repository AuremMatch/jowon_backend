from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RatingViewSet
from .views import EvaluationViewSet


urlpatterns = [
    path('', RatingViewSet.as_view({'get': 'list', 'post': 'create'}), name='conversation-list'),
     # EvaluationViewSet: list(GET) and create(POST)
    path('evaluations/', EvaluationViewSet.as_view({'get': 'list', 'post': 'create'}), name='evaluation-list'),
]