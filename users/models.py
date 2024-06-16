
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
    자기소개 = models.TextField(blank=True, null=True)
    # 회원가입 시 빼기

    깃주소 = models.URLField(blank=True, null=True)  # 깃허브 주소
    포토폴리오링크 = models.URLField(blank=True, null=True)  # 포트폴리오 링크
    연관학과 = models.CharField(max_length=100)  # 학과
    avatar = models.URLField(blank=True)

    favs = models.ManyToManyField("contests.Contest", related_name="favs")

    apply = models.ManyToManyField("contests.Contest", related_name="apply")

     # JSON 필드 추가
    selected_choices = models.JSONField(default=list, blank=True)


class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='score')  # 외래 키로 User 모델과 연결
    grade = models.IntegerField(null=True)  # 학점 (실수형) => 성실도 => 낮게 
    depart = models.IntegerField(null=True)  # 학과 (정수형) => 연관학과
    credit = models.FloatField(null=True)  # 학점 (실수형) 
    in_school_award_cnt = models.IntegerField(null=True)  # 교내 수상 횟수 (정수형) => 
    out_school_award_cnt = models.IntegerField(null=True)  # 교외 수상 횟수 (정수형) =>
    national_competition_award_cnt = models.IntegerField(null=True)  # 국가대회 수상 횟수 (정수형)
    aptitude_test_score = models.IntegerField(null=True)  # 적성 테스트 점수 (정수형)
    certificate = models.IntegerField(null=True)  # 자격증 보유 여부 (정수형) => 근거
    major_field = models.IntegerField(null=True)  # 전공 분야 (정수형)
    codingTest_score = models.IntegerField(null=True)  # 코딩 테스트 점수 (정수형) =>


    # 부트캠프 참여여부  1 0 => 가중치높게
    # 진위여부 파악 => bbs
    # 멘토 멘티 => 
    # 외국인교환학생

    # 깃허브 스타 프로그래머스 백준 가산점 부여 54321 성실도


    # 만약에 이팀 성적이 좋았을 경우 가중치 점수 더 추가해서 인공지능 정확도 올리기

    # 경험해본적 없음 추가

    # 지역 상관여부
    

    # 자격증 섹션 여러개두기

    # 6각형 능력치파악
    # 성실도 경험 성과 


class UserContestChoices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey("contests.Contest", on_delete=models.CASCADE)
    selected_choices = models.JSONField(default=list)
