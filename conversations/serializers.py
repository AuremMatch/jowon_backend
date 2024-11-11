from rest_framework import serializers
from .models import Conversation, Message
from users.serializers import UserSerializer
from users.models import User



class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    pendingParticipants = UserSerializer(many=True, read_only=True)  # pendingParticipants를 UserSerializer로 직렬화
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        exclude = ('주최', '응모분야', '참가대상', '접수기간', '접수방법', '시상금')


class PendingParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # 적절한 사용자 모델로 교체
        fields = ["이름", "학번"]  # 필요한 필드 포함