from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
           
        )
        
class PrivateUserSerializer(serializers.ModelSerializer):
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

    



