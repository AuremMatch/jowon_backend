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

class ConversationViewSet(ModelViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all().order_by('-created')[:8]
    permission_classes = [AllowAny]
    pagination_class = None 

    def create(self, request, *args, **kwargs):
        contest_id = request.data.get('contest_id')
        image_url = request.data.get('image')
        ai_response = request.data.get('ai_response')  # AI 응답 데이터 가져오기
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

        if matching_type == 'same':
            # 현재 사용자의 예측값 가져오기
            current_user_id = request.user.id
            my_prediction_value = None

            for applicant in applicants:
                if applicant.get('id') == current_user_id:
                    my_prediction_value = applicant.get('predictions', {}).get('GCGF 혁신 아이디어 공모', 0)  # 예측값 설정
                    break

            if my_prediction_value is None:
                return Response({'error': 'User prediction value not found.'}, status=status.HTTP_400_BAD_REQUEST)

            # 예측값을 기준으로 정렬
            applicants.sort(key=lambda x: abs(x.get('predictions', {}).get('GCGF 혁신 아이디어 공모', 0) - my_prediction_value))

            # 비슷한 예측값을 가진 사용자들을 3명씩 묶어서 여러 개의 팀 생성
            created_conversations = []
            for i in range(0, len(applicants), 3):
                team = applicants[i:i + 3]
                selected_user_ids = [user.get('id') for user in team]

                data = request.data.copy()
                if image_url:
                    data['image'] = image_url
                data['ai_response'] = team  # 선택된 사용자들의 예측값을 serializer에 추가
                data['matching_type'] = matching_type  # matching_type을 data에 추가

                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                conversation = serializer.save()

                conversation.participants.set(selected_user_ids)
                conversation.save()

                created_conversations.append(serializer.data)

            headers = self.get_success_headers(serializer.data)

            # 디버깅: 반환할 데이터를 출력
            for conversation in created_conversations:
                print("Response data:", conversation)
                print("AI Response data:", data['ai_response'])  # 추가된 디버깅 코드

            return Response(created_conversations, status=status.HTTP_201_CREATED, headers=headers)

        elif matching_type == 'random':
            # 참가자 리스트를 무작위로 섞음
            import random
            random.shuffle(applicants)

            # 참가자들을 4명씩 묶어서 한 팀 생성
            team = applicants[:4]
            selected_user_ids = [user.get('id') for user in team]

            data = request.data.copy()
            if image_url:
                data['image'] = image_url
            data['ai_response'] = team  # 선택된 사용자들의 예측값을 serializer에 추가
            data['matching_type'] = matching_type  # matching_type을 data에 추가

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            conversation = serializer.save()

            conversation.participants.set(selected_user_ids)
            conversation.save()

            headers = self.get_success_headers(serializer.data)

            # 디버깅: 반환할 데이터를 출력
            print("Response data:", serializer.data)
            print("AI Response data:", data['ai_response'])  # 추가된 디버깅 코드

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # `data`에 `image` URL과 기타 데이터를 추가하여 serializer에 전달
        data = request.data.copy()
        if image_url:
            data['image'] = image_url
        if ai_response:
            data['ai_response'] = ai_response  # 요청 데이터에서 직접 ai_response를 추가
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
        print("AI Response data:", data['ai_response'])  # 추가된 디버깅 코드

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['delete'])
    def destroy(self, request, pk=None):
        try:
            conversation = self.get_object()
            conversation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)




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
