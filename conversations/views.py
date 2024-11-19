from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Conversation
from .serializers import ConversationSerializer
from rest_framework.decorators import action
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import MessageSerializer
from rest_framework import viewsets
from .models import Message
from django.shortcuts import get_object_or_404
from contests.views import ContestViewSet
from contests.models import Contest
import requests
import random
from users.models import Coding
from .serializers import ConversationSerializer
from .serializers import PortfolioSerializer
from .models import Portfolio

class ConversationViewSet(ModelViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all().order_by('-created')
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def update(self, request, *args, **kwargs):
        # 기존 대화 객체를 가져옴
        
        conversation = self.get_object()

        # 요청 데이터에서 participants 가져오기
        new_participants = request.data.get('participants', [])
        contest_id = request.data.get('contest_id')

        if not isinstance(new_participants, list):
            return Response({'error': 'Participants should be a list.'}, status=status.HTTP_400_BAD_REQUEST)

        # 기존 참가자 가져오기
        current_participants = list(conversation.participants.all().values_list('id', flat=True))

        # 중복되지 않게 새로운 참가자 추가
        updated_participants = list(set(current_participants + new_participants))

        # 참가자 업데이트
        conversation.participants.set(updated_participants)
         # contest_id가 제공된 경우 conversation에 추가
        if contest_id is not None:
            conversation.contest_id = contest_id

        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'get'])
    def add_portfolio(self, request, pk=None):
        # 특정 Conversation 객체 가져오기
        conversation = self.get_object()

        if request.method == 'POST':
            # 요청 데이터 가져오기
            title = request.data.get('title')
            description = request.data.get('description', '')
            image = request.data.get('image', None)
            document = request.FILES.get('document', None)
            link = request.data.get('link', None)

            # Portfolio 객체 생성 및 Conversation에 연결
            portfolio = Portfolio.objects.create(
                title=title,
                description=description,
                image=image,
                document=document,
                link=link
            )
                # Many-to-Many 관계에 포트폴리오 추가
            conversation.portfolio.add(portfolio)  # .add()를 사용하여 추가

            # 응답 반환
            portfolio_serializer = PortfolioSerializer(portfolio)
            return Response(portfolio_serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'GET':
            # Conversation에 연결된 모든 Portfolio 정보 반환
            portfolios = conversation.portfolio.all()  # .all()로 모든 객체 가져오기
            if portfolios.exists():
                portfolio_serializer = PortfolioSerializer(portfolios, many=True)
                return Response(portfolio_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "No Portfolios found for this Conversation."},
                    status=status.HTTP_404_NOT_FOUND
                )

      # 대기 중인 팀원을 추가하는 메서드
    @action(detail=True, methods=["get","post"])
    def add_pending_participant(self, request, pk=None):
        conversation = self.get_object()

        if request.method == "GET":
            # GET 요청: 대기 중인 팀원의 목록 조회
            pending_participants = conversation.pendingParticipants.all()
            serializer = self.serializer_class(pending_participants, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "POST":
            # POST 요청: 대기 중인 팀원 추가
            user_id = request.data.get('user_id')
            if not user_id:
                return Response({'error': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
            if user_id in conversation.pendingParticipants.values_list('id', flat=True):
                return Response({'message': 'User is already in pending participants.'}, status=status.HTTP_200_OK)

            conversation.pendingParticipants.add(user_id)
            conversation.save()

            serializer = self.get_serializer(conversation)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # 대기 중인 팀원을 수락하여 정식 참가자로 추가하는 메서드
    @action(detail=True, methods=["get","post"])
    def accept_pending_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'error': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if user_id not in conversation.pendingParticipants.values_list('id', flat=True):
            return Response({'error': 'User is not in pending participants.'}, status=status.HTTP_404_NOT_FOUND)

        # 대기 중인 팀원에서 제거하고 정식 참가자로 추가
        conversation.pendingParticipants.remove(user_id)
        conversation.participants.add(user_id)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        contest_id = request.data.get('contest_id')
        image_url = request.data.get('image')
       
        graph = request.data.get('graph')  # 그래프 데이터 가져오기
        matching_type = request.data.get('matching_type')  # 매칭 유형을 요청 데이터에서 가져옴
        participants = request.data.get('participants')  # 참가자 데이터 가져오기

        if not contest_id:
            return Response({'error': 'Contest ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        applicants = []

        if matching_type in ['same', 'random']:
            # Contest의 참가자 리스트를 가져오기 위해 HTTP 요청을 보냄
            url = f'http://127.0.0.1:8000/contests/{contest_id}/applicants/'
            response = requests.get(url)
            if response.status_code != 200:
                return Response({'error': 'Failed to fetch applicants.'}, status=response.status_code)

            applicants = response.json()

        if matching_type == 'random':
            current_user = request.user
            current_coding = get_object_or_404(Coding, user=current_user)
            
            # 모든 신청자들 중에서 현재 사용자를 제외한 사람들의 코딩 점수를 가져옵니다.
            applicants = Coding.objects.filter(user__apply__id=contest_id).exclude(user=current_user)

            # 현재 사용자의 각 항목별 점수 비교하여 가장 낮은 항목 두 개를 찾습니다.
            score_diffs = {
                "backend_score": current_coding.backend_score,
                "frontend_score": current_coding.frontend_score,
                "design_score": current_coding.design_score,
                "deploy_score": current_coding.deploy_score,
                "ppt_score": current_coding.ppt_score,
            }
            weakest_areas = sorted(score_diffs, key=score_diffs.get)[:2]  # 가장 낮은 두 항목을 선택

            # 첫 번째 약점에 대해 높은 점수를 가진 팀원들 찾기 (슬라이싱 전에 필터링 수행)
            best_matches_first = applicants.order_by(f'-{weakest_areas[0]}')[:2]

            # 두 번째 약점에 대해 높은 점수를 가진 팀원들 찾기 (필터링 먼저 수행)
            best_matches_second = applicants.exclude(user__in=[match.user for match in best_matches_first]).order_by(f'-{weakest_areas[1]}')[:1]

            # 최종적으로 매칭된 팀원들 (현재 사용자 + 3명)
            final_matches = list(best_matches_first) + list(best_matches_second)

            if len(final_matches) < 2:
                return Response({'error': 'No suitable match found.'}, status=status.HTTP_404_NOT_FOUND)

            # 매칭된 사용자의 코딩 점수 출력 (로그)
            print(f"Current User: {current_user.username}, Weakest Areas: {weakest_areas}")
            for area in weakest_areas:
                print(f"Weak Area: {area}, Score: {score_diffs[area]}")
            for match in final_matches:
                print(f"Matched User: {match.user.username}, {weakest_areas[0]} Score: {getattr(match, weakest_areas[0])}, {weakest_areas[1]} Score: {getattr(match, weakest_areas[1])}")

            # 팀 매칭 결과를 저장하기 위해 데이터 준비
            selected_user_ids = [current_user.id] + [match.user.id for match in final_matches]
            data = request.data.copy()
            data['participants'] = selected_user_ids  # 선택된 참가자들의 ID 설정

            # 저장 및 응답
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            conversation = serializer.save()

            conversation.participants.set(selected_user_ids)
            conversation.save()

            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # elif matching_type == 'random':
        #     # 참가자 리스트를 무작위로 섞음
        #     import random
        #     random.shuffle(applicants)

        #     # 참가자들을 4명씩 묶어서 한 팀 생성
        #     team = applicants[:4]
        #     selected_user_ids = [user.get('id') for user in team]

        #     data = request.data.copy()
        #     if image_url:
        #         data['image'] = image_url
        #     data['ai_response'] = team  # 선택된 사용자들의 예측값을 serializer에 추가
        #     data['matching_type'] = matching_type  # matching_type을 data에 추가

        #     serializer = self.get_serializer(data=data)
        #     serializer.is_valid(raise_exception=True)
        #     conversation = serializer.save()

        #     conversation.participants.set(selected_user_ids)
        #     conversation.save()

        #     headers = self.get_success_headers(serializer.data)

        #     # 디버깅: 반환할 데이터를 출력
        #     print("Response data:", serializer.data)
        #     print("AI Response data:", data['ai_response'])  # 추가된 디버깅 코드

        #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # `data`에 `image` URL과 기타 데이터를 추가하여 serializer에 전달
        data = request.data.copy()
        if image_url:
            data['image'] = image_url
       
        if graph:
            data['graph'] = graph  # 요청 데이터에서 직접 graph를 추가

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()

        # participants 데이터를 설정
        if participants:
            conversation.participants.set(participants)
        conversation.save()

        headers = self.get_success_headers(serializer.data)

        # 디버깅: 반환할 데이터를 출력
        print("Response data:", serializer.data)
        

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['delete'])
    def destroy(self, request, pk=None):
        try:
            conversation = self.get_object()
            conversation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my(self, request):
        user = request.user
        conversations = Conversation.objects.filter(participants=user).order_by('-created')
        serializer = self.get_serializer(conversations, many=True)
        return Response(serializer.data)



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = None

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id is not None:
            return Message.objects.filter(conversation_id=conversation_id)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        if not conversation_id:
            return Response({'error': 'Conversation ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
