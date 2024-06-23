from rest_framework import serializers
from .models import Contest, Like
from .models import ContestApplication
from survey.serializers import SurveySerializer  # surveys 앱의 Serializer를 가져옵니다.

class ContestSerializer(serializers.ModelSerializer):
    survey = SurveySerializer()  # SurveySerializer를 포함하여 설문지 정보를 직렬화합니다.
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

