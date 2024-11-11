# views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import Proposal, Notification
from .serializers import ProposalSerializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import F, Value, CharField, ExpressionWrapper
from django.db.models.functions import Length

from conversations.models import Conversation

class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        proposal = self.get_object()
        proposal.receiver = request.user
        proposal.save()
        Notification.objects.create(user=proposal.sender, message=f'{request.user.username}님이 제의를 수락했습니다.')
        return Response({'message': 'Proposal accepted.'})

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.order_by('-created_at')
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
   
    pagination_class = None 

    def create(self, request, *args, **kwargs):
        # 요청 데이터에서 필요한 정보 추출
        message = request.data.get('message')
        image = request.data.get('image')  # 이미지 필드 추가
        
        conversation_id = request.data.get('conversation_id')  # conversation_id 필드 추가

        # conversation_id 출력
        print("Conversation ID:", conversation_id)
        
        # 필수 필드가 있는지 확인
        if not message:
            return Response({"error": "Message field is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 현재 로그인한 사용자를 가져오거나, 필요한 경우 request.user.id를 사용하여 사용자 ID를 설정
            user = request.user
        except AttributeError:
            return Response({"error": "User authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)
        
         # 연결된 Conversation 설정
        conversation = get_object_or_404(Conversation, id=conversation_id)

         

        # Notification 객체 생성
        notification = Notification.objects.create(user=user, message=message, image=image,  conversation=conversation )
   
        # 생성된 Notification 객체를 시리얼라이즈하여 응답
        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], url_path='short-messages')
    def short_messages(self, request):
        # message 길이가 5 이하인 알림 필터링
        short_messages = Notification.objects.annotate(message_length=Length('message')).filter(message_length__lte=5).order_by('-created_at')
        serializer = self.get_serializer(short_messages, many=True)
        return Response(serializer.data)