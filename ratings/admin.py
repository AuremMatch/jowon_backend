from django.contrib import admin
from . import models


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):

    """ Message Admin Definition """

    pass


@admin.register(models.Evaluation)
class EvaluationAdmin(admin.ModelAdmin):

    """ Message Admin Definition """

    pass