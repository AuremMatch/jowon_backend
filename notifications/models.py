from django.db import models

class Proposal(models.Model):
    sender = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='sent_proposals')
    receiver = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='received_proposals')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='notifications')
    image = models.URLField(null=True)  # 사진 (URL 형식)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)