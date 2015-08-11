from django.contrib import admin
from mgr.models import Department, FieldOfStudy, Question, Answer, FieldOfQuestion, UserProfile, CustomTest, Statistic


class DepartmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Department, DepartmentAdmin)


class FieldOfStudyAdmin(admin.ModelAdmin):
    pass
admin.site.register(FieldOfStudy, FieldOfStudyAdmin)


class FieldOfQuestionAdmin(admin.ModelAdmin):
    pass
admin.site.register(FieldOfQuestion, FieldOfQuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Answer, AnswerAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['is_prepared', 'approved_by_admin']
admin.site.register(Question, QuestionAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ["question_prepared"]
admin.site.register(UserProfile, UserProfileAdmin)


class CustomTestAdmin(admin.ModelAdmin):
    filter_horizontal = ['questions']
admin.site.register(CustomTest, CustomTestAdmin)


class StatisticAdmin(admin.ModelAdmin):
    pass
admin.site.register(Statistic, StatisticAdmin)
