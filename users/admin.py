from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.User, models.Score)
class ContestAdmin(admin.ModelAdmin):
        pass


