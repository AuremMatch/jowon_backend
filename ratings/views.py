from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Rating
from .serializers import RatingSerializer
from rest_framework.permissions import IsAuthenticated

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        ratee_id = request.data.get('ratee')
        activity_score = request.data.get('activity_score')
        accuracy_score = request.data.get('accuracy_score')
        teamwork_score = request.data.get('teamwork_score')
        overall_score = request.data.get('overall_score')

        # Check if any field is None
        if not ratee_id or activity_score is None or accuracy_score is None or teamwork_score is None or overall_score is None:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if int(request.user.id) == int(ratee_id):
            return Response({"error": "You cannot rate yourself."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ratee_id = int(ratee_id)
            activity_score = int(activity_score)
            accuracy_score = int(accuracy_score)
            teamwork_score = int(teamwork_score)
            overall_score = int(overall_score)
        except (ValueError, TypeError) as e:
            return Response({"error": f"Invalid value for one of the fields: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        if any(score < 1 or score > 5 for score in [activity_score, accuracy_score, teamwork_score, overall_score]):
            return Response({"error": "All scores must be between 1 and 5"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the rater has already rated the ratee
        existing_rating = Rating.objects.filter(rater=request.user, ratee_id=ratee_id).first()
        if existing_rating:
            # If a rating already exists for this rater and ratee, update it
            existing_rating.activity_score = activity_score
            existing_rating.accuracy_score = accuracy_score
            existing_rating.teamwork_score = teamwork_score
            existing_rating.overall_score = overall_score
            existing_rating.save()
            serializer = self.get_serializer(existing_rating)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # If no rating exists, create a new one
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rater=request.user, ratee_id=ratee_id, activity_score=activity_score, accuracy_score=accuracy_score, teamwork_score=teamwork_score, overall_score=overall_score)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
