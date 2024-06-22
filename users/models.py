from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices


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
    학교 = models.CharField(max_length=100)  # 학과
    avatar = models.URLField(blank=True)

    favs = models.ManyToManyField("contests.Contest", related_name="favs")

    apply = models.ManyToManyField("contests.Contest", related_name="apply")

     # JSON 필드 추가
    selected_choices = models.JSONField(default=list, blank=True)

    is_email_verified = models.BooleanField(default=False)  # 이메일 인증 여부

class MajorField(models.IntegerChoices):
    COMPUTER_SCIENCE = 1, 'Computer Science'
    ELECTRICAL_ENGINEERING = 2, 'Electrical Engineering'
    MECHANICAL_ENGINEERING = 3, 'Mechanical Engineering'

class Department(models.IntegerChoices):
    COMPUTER_SCIENCE = 1, 'Computer Science'
    ELECTRICAL_ENGINEERING = 2, 'Electrical Engineering'
    MECHANICAL_ENGINEERING = 3, 'Mechanical Engineering'

class CourseTakenChoices(models.IntegerChoices):
    COMPUTER_ENGINEERING = 1, '컴퓨터공학'
    ARTIFICIAL_INTELLIGENCE = 2, '인공지능'
    COMPUTER_SYSTEM_AND_NETWORK = 3, '컴퓨터 시스템 및 네트워크'
    NETWORK_SECURITY = 4, '네트워크 보안'
    DATABASE = 5, '데이터베이스'
    WEB_AND_APPLICATION_DEVELOPMENT = 6, '웹 및 어플리케이션 개발'
    SOFTWARE_ENGINEERING = 7, '소프트웨어 공학'

class CertificateScoreChoices(models.IntegerChoices):
    COMPUTER_ENGINEERING = 1, '정보기술자격'
    ARTIFICIAL_INTELLIGENCE = 2, '리눅스마스터'
    COMPUTER_SYSTEM_AND_NETWORK = 3, '데이터분석'
    NETWORK_SECURITY = 4, '정보통신기사'
    DATABASE = 5, '정보처리기사'
   

class Score(models.Model):
    # One-to-One relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='score')

    # 학점 (실수형)
    grade = models.FloatField(null=True)  # 학점을 실수형으로 저장

    # GitHub 커밋 횟수 (정수형)
    github_commit_count = models.IntegerField(null=True)  # GitHub 커밋 횟수를 정수형으로 저장

    # 백준 점수 (정수형)
    baekjoon_score = models.IntegerField(null=True)  # 백준 점수를 정수형으로 저장

    # 프로그래머스 점수 (정수형)
    programmers_score = models.IntegerField(null=True)  # 프로그래머스 점수를 정수형으로 저장

    # 자격증 수 (정수형)
    certificate_count = models.IntegerField(null=True)  # 자격증 수를 정수형으로 저장

    # 학년 (정수형, choices 필드 사용)
    senior = models.IntegerField(null=True) # 학년을 설정

    # 학과 (정수형, choices 필드 사용)
    depart = models.IntegerField(choices=Department.choices, null=True)  # 학과를 선택지에서 선택 가능하도록 설정

    # 수강한 과목 (정수형, choices 필드 사용)
    courses_taken = models.IntegerField(choices=CourseTakenChoices.choices, null=True)  # 수강한 과목을 선택지에서 선택 가능하도록 설정

    # 전공 분야 (정수형, choices 필드 사용)
    major_field = models.IntegerField(choices=MajorField.choices, null=True)  # 전공 분야를 선택지에서 선택 가능하도록 설정

    bootcamp_experience = models.IntegerField(choices=((1, 'Yes'), (0, 'No')), null=True)

    # 교내 수상 횟수 (정수형)
    in_school_award_cnt = models.IntegerField(null=True)  # 교내 수상 횟수를 정수형으로 저장

    # 교외 수상 횟수 (정수형)
    out_school_award_cnt = models.IntegerField(null=True)  # 교외 수상 횟수를 정수형으로 저장

    # 코딩 테스트 점수 (정수형)
    coding_test_score = models.IntegerField(null=True)  # 코딩 테스트 점수를 정수형으로 저장

    # 공식 자격증 점수 입력 
    certificate_score = models.IntegerField(choices=CertificateScoreChoices.choices, null=True) 
  

    aptitude_test_score = models.IntegerField(null=True)  # 설문조사점수를 정수형으로 저장


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
