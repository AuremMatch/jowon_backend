from django.urls import path
from .views import ProposalViewSet, NotificationViewSet

urlpatterns = [
    path('proposals/', ProposalViewSet.as_view({'get': 'list', 'post': 'create'}), name='proposal-list'),
    path('proposals/<int:pk>/', ProposalViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='proposal-detail'),
    path('proposals/<int:pk>/accept/', ProposalViewSet.as_view({'post': 'accept'}), name='proposal-accept'),
    path('', NotificationViewSet.as_view({'get': 'list', 'post': 'create'}), name='notification-list'),
    path('<int:pk>/', NotificationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='notification-detail'),
]
