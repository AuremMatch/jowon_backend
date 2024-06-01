from django.db import models
from core import models as core_models

class Proposal(models.Model):
    sender = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='sent_proposals')
    receiver = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='received_proposals')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(core_models.TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='notifications')
    image = models.URLField(null=True)  # 사진 (URL 형식)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    conversation = models.ForeignKey("conversations.Conversation", on_delete=models.CASCADE, null=True, blank=True)
   