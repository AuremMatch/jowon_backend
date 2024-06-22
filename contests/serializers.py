from rest_framework import serializers
from .models import Contest, Like
from .models import ContestApplication

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class ContestApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestApplication
        fields = ['id', 'user', 'contest', 'applied_at']

