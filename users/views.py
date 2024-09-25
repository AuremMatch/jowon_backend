from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
import os  # os 모듈 import 추가
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from . import models
from django.urls import reverse
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from contests.serializers import ContestSerializer
from contests.models import Contest
from ratings.models import Rating
from django.db.models import Avg
from .serializers import PrivateUserSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
import jwt
from django.shortcuts import get_object_or_404

from . import serializers
from rest_framework import generics

class UserViewSet(ModelViewSet):

    queryset = models.User.objects.all()
    serializer_class = PrivateUserSerializer
    


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user)  # PrivateUserSerializer 사용
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    

class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ContestSerializer(user.favs.all().order_by('-updated'), many=True).data
        return Response(serializer)

    def put(self, request):
        
        pk = request.data.get("id", None)
        user = request.user
        if pk is not None:
            try:
                room = Contest.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Contest.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class ApplyView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ContestSerializer(user.apply.all(), many=True).data
        return Response(serializer)

    def put(self, request):
        
        pk = request.data.get("id", None)
        user = request.user
        if pk is not None:
            try:
                room = Contest.objects.get(pk=pk)
                if room in user.apply.all():
                    user.apply.remove(room)
                else:
                    user.apply.add(room)
                return Response()
            except Contest.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        contest_id = request.data.get("contest_id", None)
        if contest_id is None:
            return Response({'error': 'Contest ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            contest = Contest.objects.get(pk=contest_id)
        except Contest.DoesNotExist:
            return Response({'error': 'Contest not found'}, status=status.HTTP_404_NOT_FOUND)

        users = contest.apply.all()
        results = []

        for user in users:
            try:
                score = user.score  # User 모델과 연결된 Score 모델 인스턴스 가져오기
            except models.Score.DoesNotExist:
                return Response({'error': f'Score not found for user {user.username}'}, status=status.HTTP_404_NOT_FOUND)

            student_data = {
                'grade': score.grade,
                'depart': score.depart,
                'credit': score.credit,
                'in_school_award_cnt': score.in_school_award_cnt,
                'out_school_award_cnt': score.out_school_award_cnt,
                'national_competition_award_cnt': score.national_competition_award_cnt,
                'aptitude_test_score': score.aptitude_test_score,
                'certificate': score.certificate,
                'major_field': score.major_field,
                'codingTest_score': score.codingTest_score,
            }

            # Check if all required columns are present and not None
            missing_columns = [col for col in student_data if student_data[col] is None]
            if missing_columns:
                return Response({'error': f'Missing columns: {", ".join(missing_columns)}'}, status=status.HTTP_400_BAD_REQUEST)

            prediction = predict_contest_winning_probabilities(student_data)
            results.append({
                'user_id': user.id,
                'user_name': user.이름,
                'predictions': prediction
            })

        return Response(results)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError
        
class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({
                "id": user.id,
                "이름": user.이름,
                "학번": user.학번,
                "학과": user.학과,
                "대회참가횟수": user.대회참가횟수,
                "총받은상금": user.총받은상금,
                "예상상금": user.예상상금,
                "개발경력": user.개발경력,
                "깃주소": user.깃주소,
                "포토폴리오링크": user.포토폴리오링크,
                
                # 필요한 다른 사용자 데이터 추가
            })
        else:
            return Response({"error": "wrong password"})


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self):
        logout(self.request)
        return Response({"ok": "bye!"})
    
class SignUpViewSet(ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
             # 토큰 생성 및 저장
            token, created = Token.objects.get_or_create(user=user)
            # 이메일 인증 메일 보내기
            self.send_verification_email(user, token.key)
            return Response({"message": "User created successfully. Check your email for verification."},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_email(self, user, token):
        token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm='HS256')
        subject = 'Verify your email address'
        message = f'안녕하세요 {user.username}님, 이메일 인증을 완료해주세요: ' \
                  f'http://127.0.0.1:8000/users/api/signup/verify-email/{token}/'
        from_email = settings.DEFAULT_FROM_EMAIL  # 이메일 설정에 맞게 변경
        to_email = user.email
        send_mail(subject, message, from_email, [to_email])

class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded['user_id']
            user = models.User.objects.get(id=user_id)
            user.is_email_verified = True
            user.save()

            # 이메일 인증 후 홈 화면으로 리다이렉트 또는 메시지 반환
            return redirect('http://127.0.0.1:3000/')
        except jwt.ExpiredSignatureError:
            return Response({"error": "Expired token"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except models.User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)




class UpdateSelectedChoicesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        selected_choices = request.data.get('selected_choices', [])
        contest_id = request.data.get('contest_id')
        
        if not isinstance(selected_choices, list):
            return Response({'error': 'selected_choices must be a list'}, status=status.HTTP_400_BAD_REQUEST)

         # selected_choices 유효성 검사
        if not isinstance(selected_choices, list):
            return Response({'error': 'selected_choices must be a list'}, status=status.HTTP_400_BAD_REQUEST)


        # contest_id 유효성 검사
        if not contest_id:
            return Response({'error': 'contest_id is required'}, status=status.HTTP_400_BAD_REQUEST)


        # contest_id가 실제로 존재하는지 확인
        try:
            contest = Contest.objects.get(id=contest_id)
        except Contest.DoesNotExist:
            return Response({'error': 'Contest does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # UserContestChoices 객체를 찾거나 생성
        user_contest_choice, created = models.UserContestChoices.objects.get_or_create(user=user, contest=contest)
        user_contest_choice.selected_choices = selected_choices
        user_contest_choice.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ScoreViewSet(ModelViewSet):
    queryset = models.Score.objects.all()
    serializer_class = serializers.ScoreSerializer
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # 로그인된 유저를 user 필드에 설정
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def averages_performance(self, request):
        avg_data = models.Score.objects.aggregate(
            avg_grade=Avg('grade'),
            avg_github_commit_count=Avg('github_commit_count'),
            avg_baekjoon_score=Avg('baekjoon_score'),
            avg_programmers_score=Avg('programmers_score'),
            avg_certificate_count=Avg('certificate_count')
        )
        return Response(avg_data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def averages_experience(self, request):
        avg_data = models.Score.objects.aggregate(
            avg_depart=Avg('depart'),
            avg_courses_taken=Avg('courses_taken'),
            avg_major_field=Avg('major_field'),
            avg_bootcamp_experience=Avg('bootcamp_experience')
        )
        return Response(avg_data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def averages_result(self, request):
        avg_data = models.Score.objects.aggregate(
            avg_in_school_award_cnt=Avg('in_school_award_cnt'),
            avg_out_school_award_cnt=Avg('out_school_award_cnt'),
            avg_coding_test_score=Avg('coding_test_score'),
            avg_certificate_score=Avg('certificate_score')
        )
        return Response(avg_data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def user_average_scores(self, request):
        user_scores = models.Score.objects.filter(user=request.user).aggregate(
            avg_grade=Avg('grade'),
            avg_github_commit_count=Avg('github_commit_count'),
            avg_baekjoon_score=Avg('baekjoon_score'),
            avg_programmers_score=Avg('programmers_score'),
            avg_certificate_count=Avg('certificate_count'),
            avg_depart=Avg('depart'),
            avg_courses_taken=Avg('courses_taken'),
            avg_major_field=Avg('major_field'),
            avg_bootcamp_experience=Avg('bootcamp_experience'),
            avg_in_school_award_cnt=Avg('in_school_award_cnt'),
            avg_out_school_award_cnt=Avg('out_school_award_cnt'),
            avg_coding_test_score=Avg('coding_test_score'),
            avg_certificate_score=Avg('certificate_score')
        )
        return Response(user_scores)
    
class CodingScoreViewSet(ModelViewSet):
    queryset = models.Coding.objects.all()
    serializer_class = serializers.CodingSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # pk가 주어졌을 경우, 해당 사용자의 코딩 점수를 반환
        pk = self.kwargs.get('pk')
        if pk:
            try:
                return models.Coding.objects.get(pk=pk)
            except models.Coding.DoesNotExist:
                raise NotFound("No coding scores found for this user.")
        # pk가 없을 경우, 현재 로그인된 사용자의 코딩 점수를 반환
        else:
            try:
                return models.Coding.objects.get(user=self.request.user)
            except models.Coding.DoesNotExist:
                raise NotFound("No coding scores found for the current user.")

    def retrieve(self, request, pk=None):
        coding = self.get_object()
        serializer = serializers.CodingSerializer(coding)
        return Response(serializer.data)

    def update(self, request, pk=None):
        coding = self.get_object()
        serializer = serializers.CodingSerializer(coding, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        coding = self.get_object()
        coding.delete()
        return Response(status=204)

    def list(self, request):
        # 전체 사용자에 대한 코딩 점수를 조회합니다.
        queryset = models.Coding.objects.all()
        serializer = serializers.CodingSerializer(queryset, many=True)
        return Response(serializer.data)
