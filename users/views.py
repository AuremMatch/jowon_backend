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


import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
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
        serializer = ContestSerializer(user.favs.all(), many=True).data
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

    
    # def post(self, request):
    #     # POST 요청 처리 코드
    #     pk = request.data.get("pk", None)
    #     user = request.user
    #     if pk is not None:
    #         try:
    #             room = Contest.objects.get(pk=pk)
    #             if room in user.favs.all():
    #                 user.favs.remove(room)
    #             else:
    #                 user.favs.add(room)
    #             return Response(status=status.HTTP_201_CREATED)
    #         except Contest.DoesNotExist:
    #             pass
    #     return Response(status=status.HTTP_400_BAD_REQUEST)



        

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

    def post(self, request):
        logout(request)
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
    
# 대회별 최대, 최소값 설정
aptitude_test_max_min = {
    '중대한 사회 안전 이니까': (48, 12),
    '부산 도시브랜드 굿즈 디자인 공모전': (64, 16),
    '인천건축학생공모전': (68, 17),
    'GCGF 혁신 아이디어 공모': (40, 10),
    '웹 개발 콘테스트': (64, 16)
}

# 독립 변수 최대값, 최소값 설정
max_min = {
    'out_school_award_cnt': (10, 0),
    'in_school_award_cnt': (10, 0),
    'certificate_score': (12, 0),
    'certificate_count': (10, 0),
    'major_field': (13, 0),
    'depart': (3, 1),
    'grade': (4.5, 1.0),
    'senior': (4, 1),
    'coding_test_score': (5, 0),
    'courses_taken': (3, 1),  # 수정
    'github_commit_count': (50, 1),  # 추가
    'baekjoon_score': (12, 1),  # 추가
    'programmers_score': (12, 1),  # 추가
    'bootcamp_experience': (2, 1),  # 추가
}


# 모델과 스케일러를 전역 변수로 설정하여 재사용
model = None
scaler = None

def load_model_and_scaler():
    global model, scaler

    # 모델 로드
    model_path = os.path.join(settings.BASE_DIR, 'users', 'JongsulModel3.h5')
    model = tf.keras.models.load_model(model_path)

    # 데이터 로드 및 전처리
    df = pd.read_excel('jongsulData3.xlsx')
    X = df.drop(columns=list(aptitude_test_max_min.keys()))
    y = df[list(aptitude_test_max_min.keys())]

    # 스케일러 학습
    scaler = StandardScaler()
    scaler.fit(X)

# 모델과 스케일러 로드
load_model_and_scaler()

# 새로운 학생 데이터 예측
def predict_contest_winning_probabilities(new_student_data):
    new_student_df = pd.DataFrame([new_student_data])
    new_student_data_scaled = scaler.transform(new_student_df)
    predictions = model.predict(new_student_data_scaled)[0]
    
    # 확률값을 0과 100 사이의 값으로 변환
    predictions = np.clip(predictions, 0, 100)
    
    return {contest: prob for contest, prob in zip(aptitude_test_max_min.keys(), predictions)}

class PredictAPIView(APIView):

    def get(self, request):
        scores = models.Score.objects.all()
        serializer = serializers.ScoreSerializer(scores, many=True)
        return Response(serializer.data)

    def post(self, request):
        student_data = request.data

        # 데이터 검증
        print("Received data:", student_data)

        # 필드 매핑
        column_mapping = {
            'grade': 'grade',
            'github_commit_count': 'github_commit_count',
            'baekjoon_score': 'baekjoon_score',
            'programmers_score': 'programmers_score',
            'certificate_count': 'certificate_count',
            'senior': 'senior',
            'depart': 'depart',
            'courses_taken': 'courses_taken',
            'major_field': 'major_field',
            'bootcamp_experience': 'bootcamp_experience',
            'in_school_award_cnt': 'in_school_award_cnt',
            'out_school_award_cnt': 'out_school_award_cnt',
            'coding_test_score': 'coding_test_score',
            'certificate_score': 'certificate_score',
            'aptitude_test_score': 'aptitude_test_score',
           
        }

        # 데이터프레임으로 변환
        try:
            new_student_df = pd.DataFrame([student_data])
            print("DataFrame created successfully:")
            print(new_student_df)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Score 모델에 맞게 필드명 수정 및 선택
        new_student_df = new_student_df.rename(columns=column_mapping)
        selected_columns = list(column_mapping.values())

        # 필요한 열만 선택하여 정규화
        try:
            for col in selected_columns:
                if col not in new_student_df:
                    return Response({'error': f'Missing column: {col}'}, status=status.HTTP_400_BAD_REQUEST)

            # 스케일링 전 데이터 확인
            print("Data before scaling:")
            print(new_student_df[selected_columns])

            # 스케일링 적용 (스케일러를 사용하여 정규화)
            X_scaled = scaler.transform(new_student_df[selected_columns])

            # 스케일링 후 데이터 확인
            print("Data scaled successfully:")
            print(X_scaled)
        except ValueError as e:
            print("Error during scaling:")
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # 예측 수행 (로드된 모델 사용)
        try:
            predictions = predict_contest_winning_probabilities(new_student_df[selected_columns].to_dict(orient='records')[0])
            print("Prediction successful:")
            print(predictions)
        except Exception as e:
            print("Error during prediction:")
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 예측 결과 반환
        return Response(predictions)


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
    
