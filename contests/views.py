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
from .models import ContestApplication
from .serializers import ContestApplicationSerializer
from users.serializers import UserSerializer
from conversations.serializers import ConversationSerializer
import random
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from rest_framework.pagination import PageNumberPagination
import re



class CategoryViewSet(ModelViewSet):
    serializer_class = ContestSerializer
    queryset = Contest.objects.all()
    pagination_class = PageNumberPagination  # 페이지네이션 클래스 설정
    

    @action(detail=False, methods=['get'])
    def filtered_contests(self, request):
        department = request.query_params.get('연관학과')
        if department:
            filtered_contests = self.get_queryset().filter(연관학과=department)
            page = self.paginate_queryset(filtered_contests)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(filtered_contests, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Department parameter is missing"}, status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def search(self, request):
        keyword = request.query_params.get('keyword')
        if keyword:
            filtered_contests = Contest.objects.filter(제목__icontains=keyword)
            serializer = self.get_serializer(filtered_contests, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response({"error": "Keyword parameter is missing"}, status=HTTP_400_BAD_REQUEST)
        


class FilteredContests(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        department = request.user.연관학과  # 사용자의 학과 정보를 가져옵니다.
        latest_checked = request.GET.get('latest', False)  # 최신순 여부를 가져옵니다.
        filtered_contests = Contest.objects.filter(연관학과=department)
        all_contents = Contest.objects.all()
        prize_checked = request.GET.get('prize', False)  # 상금순 여부를 가져옵니다.

        # 최신순으로 필터링하는 경우
        if latest_checked:
            filtered_contests = all_contents.order_by('-id')  # created_at 필드를 기준으로 최신순으로 정렬합니다.
        

        if prize_checked:
            # 상금이 숫자로만 이루어진 경우만 필터링하고 상금 크기순으로 정렬
            filtered_contests = all_contents.order_by('-상금')

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
    
class ContestApplicationViewSet(ModelViewSet):
    serializer_class = ContestApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        contest_id = self.request.query_params.get('contest_id', None)
        if contest_id:
            return ContestApplication.objects.filter(contest__id=contest_id)
        return ContestApplication.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def list(self, request):
        contest_id = self.request.query_params.get('contest_id', None)
        queryset = ContestApplication.objects.filter(contest__id=contest_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create_conversation(self, request):
        # 지원한 사용자 중에서 무작위로 3명 선택
        contest_id = request.data.get('contest')
        applications = ContestApplication.objects.filter(contest_id=contest_id)
        participants = random.sample(list(applications.values_list('user', flat=True)), 3)

        # 대화 생성
        conversation_data = {
            'teamName': 'New Conversation Team',  # 대화 팀 이름 설정
        }


    

class ContestViewSet(ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer  # Contest 모델의 시리얼라이저가 필요합니다.

    @action(detail=True, methods=['get'])
    def applicants(self, request, pk=None):
        contest = self.get_object()
        applicants = contest.apply.all()  # 역참조를 사용하여 신청한 유저들 가져오기
        serializer = UserSerializer(applicants, many=True)
        return Response(serializer.data)

    