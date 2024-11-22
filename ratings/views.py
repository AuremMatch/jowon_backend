from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Rating
from .serializers import RatingSerializer
from .serializers import EvaluationSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Evaluation
from users.models import User

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        ratee_id = request.data.get('ratee')
        activity_score = request.data.get('activity_score')
        accuracy_score = request.data.get('accuracy_score')
        teamwork_score = request.data.get('teamwork_score')
        overall_score = request.data.get('overall_score')

        # Check if any field is None
        if not ratee_id or activity_score is None or accuracy_score is None or teamwork_score is None or overall_score is None:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if int(request.user.id) == int(ratee_id):
            return Response({"error": "You cannot rate yourself."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ratee_id = int(ratee_id)
            activity_score = int(activity_score)
            accuracy_score = int(accuracy_score)
            teamwork_score = int(teamwork_score)
            overall_score = int(overall_score)
        except (ValueError, TypeError) as e:
            return Response({"error": f"Invalid value for one of the fields: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        if any(score < 1 or score > 5 for score in [activity_score, accuracy_score, teamwork_score, overall_score]):
            return Response({"error": "All scores must be between 1 and 5"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the rater has already rated the ratee
        existing_rating = Rating.objects.filter(rater=request.user, ratee_id=ratee_id).first()
        if existing_rating:
            # If a rating already exists for this rater and ratee, update it
            existing_rating.activity_score = activity_score
            existing_rating.accuracy_score = accuracy_score
            existing_rating.teamwork_score = teamwork_score
            existing_rating.overall_score = overall_score
            existing_rating.save()
            serializer = self.get_serializer(existing_rating)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # If no rating exists, create a new one
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rater=request.user, ratee_id=ratee_id, activity_score=activity_score, accuracy_score=accuracy_score, teamwork_score=teamwork_score, overall_score=overall_score)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # 요청 데이터에서 target_user와 comment 가져오기
        target_user_id = request.data.get('target_user')
        comment = request.data.get('comment')

        # 필수 필드 검증
        if not target_user_id or not comment:
            return Response(
                {"error": "Both target_user and comment fields are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # target_user_id를 숫자로 변환
        try:
            target_user_id = int(target_user_id)
        except (ValueError, TypeError):
            return Response(
                {"error": f"Invalid target_user value: {target_user_id}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # self 평가 방지
        if request.user.id == target_user_id:
            return Response(
                {"error": "You cannot evaluate yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # target_user를 User 객체로 검색
        try:
            target_user = User.objects.get(pk=target_user_id)
        except User.DoesNotExist:
            return Response(
                {"error": f"User with ID {target_user_id} does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 기존 평가 여부 확인
        existing_evaluation = Evaluation.objects.filter(
            user=request.user,
            target_user=target_user
        ).first()

        if existing_evaluation:
            # 기존 평가 업데이트
            existing_evaluation.comment = comment
            existing_evaluation.save()
            serializer = self.get_serializer(existing_evaluation)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # 새로운 평가 생성
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, target_user=target_user, comment=comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)