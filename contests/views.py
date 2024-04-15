from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Contest
from .serializers import ContestSerializer
from rest_framework.decorators import action


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

