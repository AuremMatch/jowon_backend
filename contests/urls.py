from django.urls import path
from . import views


urlpatterns = [
    path('filtered-contests/', views.FilteredContests.as_view(), name='filtered_contests'),
    path('filtered/', views.CategoryViewSet.as_view({'get': 'filtered_contests'}), name='contest-filtered'),
    path('like-toggle/', views.LikeViewSet.as_view({'get': 'list'}), name='like-toggle'),
    path('search/', views.CategoryViewSet.as_view({'get': 'search'}), name='category-search'),
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
     path(
        'applications/<int:pk>/',
        views.ContestApplicationViewSet.as_view(
            {
                'get': 'retrieve',
                'put': 'partial_update',
                'delete': 'destroy',
            }
        ),
        name='contest-application-detail',
    ),
    path(
        'applications/',
        views.ContestApplicationViewSet.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
        name='contest-application-list',
    ),
    path(
        'applications/apply/',
        views.ContestApplicationViewSet.as_view(
            {
                'post': 'create',
            }
        ),
        name='contest-apply',
    ),

     path(
        'applications/list/',
        views.ContestApplicationViewSet.as_view({'get': 'list'}),
        name='contest-application-list',
    ),
    
]