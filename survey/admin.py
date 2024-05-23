from django.contrib import admin
from . import models


@admin.register(models.Survey, models.Question, models.Response)
class SurveyAdmin(admin.ModelAdmin):

    """ Message Admin Definition """

    pass