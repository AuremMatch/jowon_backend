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
    queryset = Conversation.objects.all().order_by('-created')
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
