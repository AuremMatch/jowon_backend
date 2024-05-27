from rest_framework import serializers
from .models import User, Score, UserContestChoices
from django.db.models import Avg
from ratings.models import Rating
from ratings.serializers import RatingSerializer
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from contests.serializers import ContestSerializer
from .models import Score


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'


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
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # password 필드를 읽기 전용으로 설정합니다.

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

        
class PrivateUserSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    ratings_received = serializers.SerializerMethodField()
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

    def get_average_rating(self, obj):
        # 사용자가 받은 별점 정보를 가져와서 평균을 계산합니다.
        ratings_received = Rating.objects.filter(ratee=obj)
        if ratings_received.exists():
            return ratings_received.aggregate(Avg('score'))['score__avg']
        return None

    def get_ratings_received(self, obj):
        # 사용자가 받은 별점 목록을 시리얼라이즈합니다.
        ratings_received = Rating.objects.filter(ratee=obj)
        return RatingSerializer(ratings_received, many=True).data

    def get_notifications(self, obj):
        # 사용자의 모든 Notification을 가져옵니다.
        notifications = Notification.objects.filter(user=obj)
        return NotificationSerializer(notifications, many=True).data




