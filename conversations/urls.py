from django.urls import path
from .views import ConversationListAPIView, MessageListAPIView

app_name = 'chat'

urlpatterns = [
    path('', ConversationListAPIView.as_view(), name='conversation-list'),
    path('<int:conversation_id>/messages/', MessageListAPIView.as_view(), name='message-list'),
]