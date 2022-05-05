from csv import list_dialects
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Professor, Student, Group, GroupStudents, Professor_Level, Request
from django import forms

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = User

    list_display = ['user_name', 'email', 'phone', 'role', 'is_active']
    list_display_links = ('user_name', 'email',)
    search_fields = ['email', 'phone', 'first_name']
    list_filter = ['is_active']
    list_per_page = 25

    readonly_fields = ('created_at', 'updated_at', 'last_login')

    fieldsets = (
        (None, {'fields': (('first_name', 'last_name'),'password', 'email', 'phone', 'role')}),
        ('Permissions', {
            'fields': ('is_active', 'is_superuser', 'is_staff',)}),
        ('Time', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone', 'password', 'password_2', 'role')}),
    )

    ordering = ['email']
    filter_horizontal = ()

    @admin.display(description='User name')
    def user_name(self, object):
        return f'{object.first_name} {object.last_name}'

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['professor_name', 'email', 'phone']
    list_display_links = ('professor_name', 'email',)
    list_per_page = 20
    list_select_related = ['user']
    ordering = ['user__email']
    @admin.display(description='Professor name')
    def professor_name(self, object):
        return f'{object.user.first_name} {object.user.last_name}'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'email', 'phone']
    list_display_links = ('student_name','email')
    list_per_page = 20
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['user__first_name__istartswith',
                    'user__phone', 'user__email']

    @admin.display(description='Student name')
    def student_name(self, object):
        return f'{object.user.first_name} {object.user.last_name}'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['professor_name', 'name']
    list_per_page = 20
    @admin.display(description='Professor name')
    def professor_name(self, object):
        return f'{object.professor.user.first_name} {object.professor.user.last_name}'

@admin.register(GroupStudents)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'professor_name', 'group']
    list_per_page = 20
    ordering = ['group']
    search_fields = ['first_name', 'group']
    @admin.display(description='Student name')
    def student_name(self, object):
        return f'{object.student.user.first_name} {object.student.user.last_name}'
    @admin.display(description='Professor name')
    def professor_name(self, object):
        return f'{object.group.professor.user.first_name} {object.group.professor.user.last_name}'

admin.site.register(Professor_Level)
admin.site.register(Request)