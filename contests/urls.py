from django.urls import path
from . import views

urlpatterns = [
    path('filtered/', views.CategoryViewSet.as_view({'get': 'filtered_contests'}), name='contest-filtered'),
    path(
        "",
        views.CategoryViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]