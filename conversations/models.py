from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):

    """ Conversation Model Definition """
    teamName = models.CharField(max_length=200, blank=True) 
    
    participants = models.ManyToManyField("users.User", blank=True)

    selected_choices = models.JSONField(default=list, blank=True)  # JSON 필드 추가

    image = models.URLField(max_length=500,null=True)  # 사진 (URL 형식)
    


    def __str__(self):
        return str(self.created)


class Message(core_models.TimeStampedModel):

    """ Message Model Definition """

    message = models.TextField()
   
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
  
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE , related_name="messages")  # 필드 이름을 conversation_id로 변경
   
   
    
    def __str__(self):
        return f"{self.user} says: {self.message}"