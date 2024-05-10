from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):

    """ Conversation Model Definition """
    teamName = models.CharField(max_length=200, blank=True) 
    
    participants = models.ManyToManyField("users.User", blank=True)

    def __str__(self):
        return str(self.created)


class Message(core_models.TimeStampedModel):

    """ Message Model Definition """

    message = models.TextField()
    contestName = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    participants = models.ManyToManyField("users.User", blank=True, related_name="hello")
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE)  # 필드 이름을 conversation_id로 변경
    text = models.TextField()  # 이 부분이 추가된 것입니다.
   
    
    def __str__(self):
        return f"{self.user} says: {self.text}"