from rest_framework import viewsets
from .models import Survey, Response
from .serializers import SurveySerializer, ResponseSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from users.models import Coding

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    pagination_class = None  

class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def perform_create(self, serializer):
        # 설문 응답을 저장합니다.
        response = serializer.save(respondent=self.request.user)
        
        # 코딩 모델의 점수를 업데이트합니다.
        coding, created = Coding.objects.get_or_create(user=self.request.user)  # User와 Coding 모델이 연결되어 있다고 가정

        # 질문에 따라 점수 업데이트
        question_text = response.question.text
        score = response.choice

        if "백엔드" in question_text:
            coding.backend_score = F('backend_score') + score
        elif "프론트" in question_text:
            coding.frontend_score = F('frontend_score') + score
        elif "디자인" in question_text:
            coding.design_score = F('design_score') + score
        elif "배포" in question_text:
            coding.deploy_score = F('deploy_score') + score
        elif "ppt" in question_text:
            coding.ppt_score = F('ppt_score') + score
        
        coding.save()

    def get_queryset(self):
        return self.queryset.filter(respondent=self.request.user)
