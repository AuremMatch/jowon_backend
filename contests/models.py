from django.db import models
from users.models import User


# Create your models here.
class KoreaContest(models.Model):

    number = models.IntegerField()  # 번호
    title = models.CharField(max_length=255)  # 제목
    related_department = models.CharField(max_length=100)  # 연관학과
    
    prize = models.CharField(max_length=100, blank=True)  # 상금
    grade = models.CharField(max_length=50, blank=True)  # 학년
    field = models.CharField(max_length=100)  # 분야
    location = models.CharField(max_length=100)  # 위치
    image = models.URLField()  # 사진 (URL 형식)

    def __str__(self):
        return self.title
    
# Create your models here.
class JunbukContest(models.Model):

    number = models.IntegerField()  # 번호
    title = models.CharField(max_length=255)  # 제목
    related_department = models.CharField(max_length=100)  # 연관학과
   
    prize = models.CharField(max_length=100, blank=True)  # 상금
    grade = models.CharField(max_length=50, blank=True)  # 학년
    field = models.CharField(max_length=100)  # 분야
    location = models.CharField(max_length=100)  # 위치
    image = models.URLField()  # 사진 (URL 형식)

    def __str__(self):
        return self.title
    
# Create your models here.
class WonkangContest(models.Model):

    number = models.IntegerField()  # 번호
    title = models.CharField(max_length=255)  # 제목
    related_department = models.CharField(max_length=100)  # 연관학과
   
    prize = models.CharField(max_length=100, blank=True)  # 상금
    grade = models.CharField(max_length=50, blank=True)  # 학년
    field = models.CharField(max_length=100)  # 분야
    location = models.CharField(max_length=100)  # 위치
    image = models.URLField()  # 사진 (URL 형식)

    def __str__(self):
        return self.title


class Contest(models.Model):

    번호 = models.IntegerField(null=True)  # 번호
    제목 = models.CharField(max_length=255, null=True)  # 제목
    연관학과 = models.CharField(max_length=100, null=True)  # 연관학과
   
    상금 = models.CharField(max_length=100, blank=True)  # 상금
    학년 = models.CharField(max_length=50, blank=True, null=True)  # 학년
    분야 = models.CharField(max_length=100, null=True)  # 분야
    위치 = models.CharField(max_length=100, null=True)  # 위치
    사진 = models.URLField(null=True)  # 사진 (URL 형식)
    참고링크 = models.URLField(null=True)
    def __str__(self):
        return self.제목


class Like(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'contest')