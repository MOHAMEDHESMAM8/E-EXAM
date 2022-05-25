from dataclasses import fields
from pyexpat import model
from django.contrib import admin
from .models import Exam, ExamGroups, ExamOptions, Result
from . import models
from django.contrib.auth.models import Group

admin.site.unregister(Group)

#admin.site.register(ExamOptions)
class ExamLine (admin.TabularInline):

    model = ExamOptions

class ExamGroupLine (admin.TabularInline):

    model = ExamGroups

    
@admin.register (Exam)
class ExamAdmin(admin.ModelAdmin):
    inlines = [ExamLine,ExamGroupLine]
    list_display = ['professor' ,'name' ,'level' ,'total' ,'time'  , 'chapter']

#@admin.register(ExamGroups)
class ExamGroupsAdmin(admin.ModelAdmin):
    list_display = ['exam' , 'group' , 'start_at' , 'end_at' , 'created_at']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student' , 'exam' ,'result' ,'created_at']
    readonly_fields = ('result',)
    def has_add_permission(self, request, obj=None):
        return False