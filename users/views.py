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


from . import serializers


class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer
    queryset = models.User.objects.all()



class Me(APIView):

   

    def get(self, request):
        user = request.user
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

        

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
    
class SignUp(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        # 필수 필드인지 확인하고 누락된 경우 ParseError 발생
        if not username or not password:
            raise ParseError
        
        # 새로운 사용자 생성
        user = models.User.objects.create_user(username=username, password=password)
        
        # 사용자 인증
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        
        # 로그인 처리
        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "Failed to authenticate user"})
        

