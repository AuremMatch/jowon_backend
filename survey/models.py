from django.db import models

class Survey(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Question(models.Model):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    CHOICE_OPTIONS = [
        (4, '매우 그렇다'),
        (3, '그렇다'),
        (2, '보통이다'),
        (1, '아니다')
    ]
    def __str__(self):
        return self.text



class Response(models.Model):
    survey = models.ForeignKey(Survey, related_name='responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='responses', on_delete=models.CASCADE)
    choice = models.IntegerField(choices=Question.CHOICE_OPTIONS)
    respondent = models.ForeignKey("users.User", related_name='responses', on_delete=models.CASCADE)
    def __str__(self):
        return f"Response from {self.respondent} to {self.question.text}"
