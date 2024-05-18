from django.db import models

from core import models as core_models

class Rating(core_models.TimeStampedModel):
    rater = models.ForeignKey("users.User", related_name='given_ratings', on_delete=models.CASCADE)
    ratee = models.ForeignKey("users.User", related_name='received_ratings', on_delete=models.CASCADE)
    score = models.PositiveIntegerField()  # 1 to 5, or any range you decide
   
    
    class Meta:
        unique_together = ('rater', 'ratee')  # Ensure a user can rate another user only once

    def __str__(self):
        return f'{self.rater} rated {self.ratee} - {self.score}'
