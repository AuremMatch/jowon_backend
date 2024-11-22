from rest_framework import serializers
from .models import Rating
from .models import Evaluation

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rater', 'ratee', 'activity_score', 'accuracy_score', 'teamwork_score', 'overall_score']
        read_only_fields = ['rater', 'created_at']

    def validate(self, data):
        rater = data.get('rater')
        ratee = data.get('ratee')
        
        if rater and ratee and rater == ratee:
            raise serializers.ValidationError("You cannot rate yourself.")
        
        return data
    
class EvaluationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')  # 현재 로그인한 사용자 ID

    class Meta:
        model = Evaluation
        fields = ['id', 'user', 'target_user', 'comment',]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_target_user(self, value):
        """
        Custom validation to ensure that the user cannot evaluate themselves.
        """
        if self.context['request'].user.id == value:
            raise serializers.ValidationError("You cannot evaluate yourself.")
        return value