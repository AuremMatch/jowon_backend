from django.contrib import admin
from . import models


@admin.register(models.Notification, models.Proposal)
class NotificationAdmin(admin.ModelAdmin):

    """ Message Admin Definition """

    pass