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
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        exclude = ('주최', '응모분야', '참가대상', '접수기간', '접수방법', '시상금')