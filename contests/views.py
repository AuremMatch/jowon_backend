from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Contest, Like
from .serializers import ContestSerializer, LikeSerializer
from rest_framework.decorators import action
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class CategoryViewSet(ModelViewSet):

    serializer_class = ContestSerializer
    queryset = Contest.objects.all()

    @action(detail=False, methods=['get'])
    def filtered_contests(self, request):
        department = request.query_params.get('연관학과')
        if department:
            filtered_contests = self.get_queryset().filter(연관학과=department)
            serializer = self.get_serializer(filtered_contests, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Department parameter is missing"}, status=400)

    @action(detail=False, methods=['get'])
    def search(self, request):
        keyword = request.query_params.get('keyword')
        if keyword:
            # 제목에 특정 키워드를 포함하는 Contest 객체들을 필터링합니다.
            filtered_contests = Contest.objects.filter(제목__icontains=keyword)
            serializer = self.get_serializer(filtered_contests, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response({"error": "Keyword parameter is missing"}, status=HTTP_400_BAD_REQUEST)

class FilteredContests(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        department = request.user.연관학과  # 사용자의 학과 정보를 가져옵니다.
        filtered_contests = Contest.objects.filter(연관학과=department)
        serializer = ContestSerializer(filtered_contests, many=True)
        return Response(serializer.data)

class LikeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def create(self, request):
        user = request.user
        contest_id = request.data.get('contest')
        contest = Contest.objects.get(id=contest_id)
        serializer = self.serializer_class(data={'user': user.id, 'contest': contest_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)