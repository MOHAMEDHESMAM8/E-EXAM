from django.contrib import admin
from .models import Exam, ExamOptions, ExamGroups, Result

admin.site.register(Exam)
admin.site.register(ExamOptions)
admin.site.register(ExamGroups)
admin.site.register(Result)