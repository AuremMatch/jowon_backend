
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  
    이름 = models.CharField(max_length=100)  # 이름
    학번 = models.CharField(max_length=100)  # 학번
    학과 = models.CharField(max_length=100)  # 학과

    # 학점 = models.CharField(max_length=100) 
    # 대학교= models.CharField(max_length=100) 
    # 성별 = models.CharField(max_length=100) 

    대회참가횟수 = models.IntegerField(default=0)  # 대회 참가 횟수
    총받은상금 = models.IntegerField(default=0)  # 총 받은 상금
    예상상금 = models.IntegerField(default=0)  # 예상 상금

    개발경력 = models.TextField(blank=True, null=True)  # 개발 경력
    # 회원가입 시 빼기

    깃주소 = models.URLField(blank=True, null=True)  # 깃허브 주소
    포토폴리오링크 = models.URLField(blank=True, null=True)  # 포트폴리오 링크
    연관학과 = models.CharField(max_length=100)  # 학과
    avatar = models.URLField(blank=True)

    favs = models.ManyToManyField("contests.Contest", related_name="favs")

    apply = models.ManyToManyField("contests.Contest", related_name="apply")


   