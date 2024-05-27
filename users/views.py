from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from . import models
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from contests.serializers import ContestSerializer
from contests.models import Contest
from ratings.models import Rating
from django.db.models import Avg
from .serializers import PrivateUserSerializer


from . import serializers


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
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # 사용자 인증
            user = authenticate(
                request,
                username=request.data['username'],
                password=request.data['password'],
            )
            
            # 로그인 처리
            if user:
                login(request, user)
                return Response({"ok": "Welcome!"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Failed to authenticate user"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

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
    

