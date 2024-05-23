from rest_framework import viewsets
from .models import Survey, Response
from .serializers import SurveySerializer, ResponseSerializer
from rest_framework.permissions import IsAuthenticated

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
        serializer.save(respondent=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(respondent=self.request.user)
