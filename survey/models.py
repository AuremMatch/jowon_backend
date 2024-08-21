from django.db import models

class Survey(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Question(models.Model):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    CHOICE_OPTIONS = [
        (5, '매우잘한다'),
        (4, '잘한다'),
        (3, '보통이다'),
        (2, '조금 할줄안다'),
        (1, '경험 해본적 없다')
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
