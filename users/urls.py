from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [

    path("me/", views.Me.as_view()),
    path("me/favs/", views.FavsView.as_view()),
    path("me/apply/", views.ApplyView.as_view()),
    path("token-login", obtain_auth_token),
    path("change-password", views.ChangePassword.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path("@<str:username>", views.PublicUser.as_view()),
    path(
        "",
        views.UserViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>",
        views.UserViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),

    path('update-selected-choices/', views.UpdateSelectedChoicesView.as_view(), name='update-selected-choices'),
]