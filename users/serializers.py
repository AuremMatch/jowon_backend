from rest_framework import serializers
from .models import User
from django.db.models import Avg
from ratings.models import Rating
from ratings.serializers import RatingSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
           
        )
        
class PrivateUserSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    ratings_received = serializers.SerializerMethodField()

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



