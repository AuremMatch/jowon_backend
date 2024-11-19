from django.db import models
from core import models as core_models


class Portfolio(core_models.TimeStampedModel):
    # 포트폴리오 관련 필드 정의
    title = models.CharField(max_length=255)  # 포트폴리오 제목
    description = models.TextField(blank=True)  # 포트폴리오 설명
    image = models.URLField(max_length=1000, null=True, blank=True)  # 이미지 URL
    document = models.FileField(upload_to='documents/', null=True, blank=True)  # 파일 업로드
    link = models.URLField(max_length=1000, null=True, blank=True)  # 관련 링크

    def __str__(self):
        return self.title


class Conversation(core_models.TimeStampedModel):
    MATCHING_TYPE_CHOICES = [
        ('random', 'Random Matching'),
        ('top_two', 'Top Two Matching'),
        ('same', 'Same Matching'),
    ]

    matching_type = models.CharField(max_length=10, choices=MATCHING_TYPE_CHOICES, default='random')

    """ Conversation Model Definition """
    teamName = models.CharField(max_length=200, blank=True) 
    
    participants = models.ManyToManyField("users.User", blank=True)

    pendingParticipants = models.ManyToManyField("users.User", related_name="pending_conversations", blank=True)  # 추가된 필드

    selected_choices = models.JSONField(default=list, blank=True)  # JSON 필드 추가

    image = models.URLField(max_length=1000,null=True)  # 사진 (URL 형식)

    contest_id = models.CharField(max_length=2, null=True, blank=True);

    # ForeignKey로 Portfolio 연결
    portfolio = models.ManyToManyField(
        'Portfolio', 
        
        related_name="conversations",
        null=True, 
        blank=True
    )


    주최 = models.CharField(max_length=200, blank=True) 
    응모분야 = models.CharField(max_length=200, blank=True) 
    참가대상 = models.CharField(max_length=200, blank=True) 
    접수기간 = models.CharField(max_length=200, blank=True) 
    접수방법 = models.CharField(max_length=200, blank=True) 
    시상금 = models.CharField(max_length=200, blank=True) 
    

    ai_response = models.JSONField(null=True, blank=True)  # AI 모델 응답을 저장할 필드
    graph = models.JSONField(null=True, blank=True) 

    def __str__(self):
        return str(self.created)


class Message(core_models.TimeStampedModel):

    """ Message Model Definition """
    message = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE , related_name="messages")  # 필드 이름을 conversation_id로 변경
   
    
    def __str__(self):
        return f"{self.user} says: {self.message}"
    

