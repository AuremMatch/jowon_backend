from django.contrib import admin
from .models import User, Score

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'grade', 'depart', 'credit', 'in_school_award_cnt', 'out_school_award_cnt', 'national_competition_award_cnt', 'aptitude_test_score', 'certificate', 'major_field', 'codingTest_score')

    def user_name(self, obj):
        return obj.user.이름  # Score 모델의 user 필드의 이름 값을 반환

    user_name.short_description = 'User Name'  # 컬럼 헤더 이름 설정