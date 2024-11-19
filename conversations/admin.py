from django.contrib import admin
from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ Message Admin Definition """

    pass

@admin.register(models.Portfolio)
class PortofolioAdmin(admin.ModelAdmin):

    """ Message Admin Definition """

    pass


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """ Conversation Admin Definition """

    list_display = ('teamName',)  # 표시할 필드를 지정합니다. 튜플 형식으로 지정합니다.