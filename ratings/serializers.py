from rest_framework import serializers
from .models import Rating

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