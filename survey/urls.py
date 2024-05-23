from django.urls import path
from .views import SurveyViewSet, ResponseViewSet

survey_list = SurveyViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

survey_detail = SurveyViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

response_list = ResponseViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

response_detail = ResponseViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', survey_list, name='survey-list'),
    path('<int:pk>', survey_detail, name='survey-detail'),
    path('responses/', response_list, name='response-list'),
    path('responses/<int:pk>/', response_detail, name='response-detail'),
]
