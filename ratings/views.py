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

    def perform_create(self, serializer):
        serializer.save(rater=self.request.user)

    def create(self, request, *args, **kwargs):
        ratee_id = request.data.get('ratee')
        if not ratee_id:
            return Response({"error": "ratee field is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.id == ratee_id:
            return Response({"error": "You cannot rate yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)