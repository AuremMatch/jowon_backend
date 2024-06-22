from django.db import models
from core import models as core_models

class Rating(core_models.TimeStampedModel):
    rater = models.ForeignKey("users.User", related_name='given_ratings', on_delete=models.CASCADE)
    ratee = models.ForeignKey("users.User", related_name='received_ratings', on_delete=models.CASCADE)
    activity_score = models.PositiveIntegerField(null=True)  # 팀활동 성실도
    accuracy_score = models.PositiveIntegerField(null=True)  # 업무 정확도
    teamwork_score = models.PositiveIntegerField(null=True)  # 팀원과의 화합도
    overall_score = models.PositiveIntegerField(null=True)  # 전체 별점
    
    class Meta:
        unique_together = ('rater', 'ratee')  # Ensure a user can rate another user only once

    def __str__(self):
        return f'{self.rater} rated {self.ratee} - {self.overall_score}'
