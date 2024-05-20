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
        rater_id = request.data.get('rater')  
        
        if not ratee_id:
            return Response({"error": "ratee field is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not rater_id:
            rater_id = request.user.id  # 'rater' 필드가 없으면 현재 로그인된 사용자를 사용
        
        try:
            # 'rater' 필드를 요청 데이터에서 가져오고, 존재하지 않으면 기본값으로 설정
            rater_id = int(rater_id)
        except ValueError:
            return Response({"error": "Invalid value for 'rater'"}, status=status.HTTP_400_BAD_REQUEST)
        
        if int(rater_id) == int(ratee_id):
            return Response({"error": "You cannot rate yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
        data['rater'] = rater_id
        
        return super().create(request, *args, data=data, **kwargs)