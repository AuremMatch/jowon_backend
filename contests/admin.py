from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.JunbukContest, models.KoreaContest, models.WonkangContest, models.Contest)
class ContestAdmin(admin.ModelAdmin):
        pass


