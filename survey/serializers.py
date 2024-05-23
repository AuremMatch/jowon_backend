from rest_framework import serializers
from .models import Survey, Question, Response


class QuestionSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'choices', 'survey']  # 'choices'와 'survey'를 명시적으로 추가
    
    def get_choices(self, obj):
        return Question.CHOICE_OPTIONS
    
class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = '__all__'

class ResponseSerializer(serializers.ModelSerializer):

    respondent = serializers.ReadOnlyField(source='respondent.username')
    class Meta:
        model = Response
        fields = '__all__'