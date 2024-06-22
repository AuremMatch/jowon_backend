from rest_framework import serializers
from .models import User, Score, UserContestChoices
from django.db.models import Avg
from ratings.models import Rating
from ratings.serializers import RatingSerializer
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from contests.serializers import ContestSerializer
from .models import Score
from django.core.mail import send_mail
from django.conf import settings
import jwt


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'

        read_only_fields = ('user',)  # user 필드를 read_only로 설정


class UserContestChoicesSerializer(serializers.ModelSerializer):
    contest = ContestSerializer()
    class Meta:
        model = UserContestChoices
        fields = ['contest', 'selected_choices']

class UserSerializer(serializers.ModelSerializer):
    score = ScoreSerializer(read_only=True)  # ScoreSerializer 추가
    choices_by_contest = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = (
            "password",
           
        )
    def get_choices_by_contest(self, obj):
        user_choices = UserContestChoices.objects.filter(user=obj)
        return UserContestChoicesSerializer(user_choices, many=True).data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class SignUpSerializer(serializers.ModelSerializer):
    학교 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email', '학교']
        extra_kwargs = {'password': {'write_only': True}}  # password 필드를 읽기 전용으로 설정합니다.

    def create(self, validated_data):
        학교 = validated_data.pop('학교')
       
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            학교=학교,
            is_active=False  # 계정을 비활성화 상태로 생성
        )
  

        return user

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('rater', 'activity_score', 'accuracy_score', 'teamwork_score', 'overall_score')

        
class PrivateUserSerializer(serializers.ModelSerializer):
    
    received_ratings = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
   
    notifications = serializers.SerializerMethodField()
    score = ScoreSerializer(read_only=True)  # ScoreSerializer 추가

    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
           
        )
        

    def get_received_ratings(self, obj):
        # 사용자가 받은 모든 평가 정보를 가져옵니다.
        ratings_received = Rating.objects.filter(ratee=obj)
        return RatingSerializer(ratings_received, many=True).data
    
    def get_average_rating(self, obj):
        ratings_received = Rating.objects.filter(ratee=obj)
        if ratings_received.exists():
            avg_activity_score = ratings_received.aggregate(Avg('activity_score'))['activity_score__avg'] or 0
            avg_accuracy_score = ratings_received.aggregate(Avg('accuracy_score'))['accuracy_score__avg'] or 0
            avg_teamwork_score = ratings_received.aggregate(Avg('teamwork_score'))['teamwork_score__avg'] or 0
            avg_overall_score = ratings_received.aggregate(Avg('overall_score'))['overall_score__avg'] or 0
            return (avg_activity_score + avg_accuracy_score + avg_teamwork_score + avg_overall_score) / 4
        return 0
    

    def get_notifications(self, obj):
        # 사용자의 모든 Notification을 가져옵니다.
        notifications = Notification.objects.filter(user=obj)
        return NotificationSerializer(notifications, many=True).data

    


class PredictResultSerializer(serializers.Serializer):
    aptitude_test_max_min = serializers.DictField(child=serializers.FloatField())
    predictions = serializers.DictField(child=serializers.FloatField())