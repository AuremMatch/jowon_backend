from rest_framework import serializers
from .models import Conversation, Message
from users.serializers import UserSerializer




class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)  # Conversation에 연결된 모든 Message를 시리얼라이즈하는 부분

    class Meta:
        model = Conversation
        fields = ['id', 'teamName', 'participants', 'messages']