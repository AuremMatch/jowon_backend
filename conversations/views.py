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

class ConversationViewSet(ModelViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all().order_by('-created')
    permission_classes = [AllowAny]
    pagination_class = None 

    def create(self, request, *args, **kwargs):
        contest_id = request.data.get('contest_id')
        image_url = request.data.get('image')
        ai_response = request.data.get('ai_response')  # AI 응답 데이터 가져오기
        
        if not contest_id:
            return Response({'error': 'Contest ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Contest의 참가자 리스트를 가져오기 위해 HTTP 요청을 보냄
        url = f'http://127.0.0.1:8000/contests/{contest_id}/applicants/'
        response = requests.get(url)
        if response.status_code != 200:
            return Response({'error': 'Failed to fetch applicants.'}, status=response.status_code)
        
        applicants = response.json()
        user_ids = [applicant['id'] for applicant in applicants]
        
        # `data`에 `image` URL을 추가하여 serializer에 전달
        data = request.data.copy()
        if image_url:
            data['image'] = image_url
        if ai_response:
            data['ai_response'] = ai_response
        

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()

        conversation.participants.set(user_ids)
        conversation.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
    


class MessageViewSet(viewsets.ModelViewSet):

    
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = None 

    def create(self, request, *args, **kwargs):
       
     
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # 현재 요청을 보낸 사용자를 메시지의 소유자로 설정
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
