from django.contrib import admin

from . import models

from .models import Question, Answer


#admin.site.register(Answer)

class QuestionLine(admin.StackedInline):
    model = models.Answer
    min_num = 1
    max_num = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionLine]
    list_display = ['professor','text' , 'degree' , 'chapter' , 'is_true_false', 'difficulty', 'in_practice']