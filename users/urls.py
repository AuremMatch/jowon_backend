from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'api/signup', views.SignUpViewSet, basename='signup')

urlpatterns = [

    path("me/", views.Me.as_view()),
    path("me/favs/", views.FavsView.as_view()),
    path("me/apply/", views.ApplyView.as_view()),
    path("token-login", obtain_auth_token),
    path("change-password", views.ChangePassword.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    path('signup/', views.SignUpViewSet.as_view({'post': 'create'}), name='signup'),
    path('students/', views.PredictAPIView.as_view(), name='student-list'),
    path('students/predict/', views.PredictAPIView.as_view(), name='student-predict'),
    path("@<str:username>", views.PublicUser.as_view()),
    # 사용자 계정 활성화 링크
   
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
        "score/",
        views.ScoreViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path('averages_performance/', views.ScoreViewSet.as_view({
        'get': 'averages_performance',
    }), name='averages-performance'),
    path('averages_experience/', views.ScoreViewSet.as_view({
        'get': 'averages_experience',
    }), name='averages-experience'),
    path('averages_result/', views.ScoreViewSet.as_view({
        'get': 'averages_result',
    }), name='averages-result'),

    path('average_user/', views.ScoreViewSet.as_view({
        'get': 'user_average_scores',
    }), name='average'),
    
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
    

    path('api/auth/', include('rest_framework.urls')),
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
    path('api/signup/verify-email/<str:token>/', views.VerifyEmailView.as_view(), name='verify-email'),
]