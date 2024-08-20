from django.contrib import admin
from .models import User, Score, Coding


@admin.register(Coding)
class CodingAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'grade', 'github_commit_count', 'baekjoon_score', 'programmers_score', 'certificate_count', 'depart', 'courses_taken', 'major_field', 'bootcamp_experience', 'in_school_award_cnt', 'out_school_award_cnt', 'coding_test_score')
    list_filter = ('depart', 'major_field', 'bootcamp_experience')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    def user_name(self, obj):
        return obj.user.get_full_name() if obj.user.get_full_name() else obj.user.username

    user_name.short_description = 'User Name'

# choices 모듈에서 Department와 MajorField를 import하여 사용합니다.
