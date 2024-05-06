from rest_framework import serializers
from .models import Contest, Like

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'