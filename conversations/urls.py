from django.urls import path
from .views import ConversationViewSet, MessageViewSet

app_name = 'chat'

urlpatterns = [
    path('', ConversationViewSet.as_view({'get': 'list'}), name='conversation-list'),
    path("<int:pk>", ConversationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='message-list'),  # 메시지를 생성하기 위한 URL 패턴
    path('messages/<int:pk>/', MessageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='message-detail'),
]