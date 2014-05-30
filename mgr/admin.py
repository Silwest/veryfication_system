from django.contrib import admin
from mgr.models import Department, FieldOfStudy, Question, Answer, FieldOfQuestion


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
    pass
admin.site.register(Question, QuestionAdmin)