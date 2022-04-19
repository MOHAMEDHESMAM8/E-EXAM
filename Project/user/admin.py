from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Professor, Student
from django import forms


admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = User

    list_display = ['first_name', 'last_name',
                    'email', 'phone', 'role', 'is_active']
    search_fields = ['email__istartswith', 'phone', 'first_name__istartswith']
    list_filter = ['is_active']
    list_per_page = 25

    readonly_fields = ('created_at', 'updated_at', 'last_login')

    fieldsets = (
        (None, {'fields': (('first_name', 'last_name'),
                           'password', 'email', 'phone', 'role')}),
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


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone']
    list_per_page = 20
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone']
    list_display_links = ('first_name', 'last_name', 'email',)
    list_per_page = 20
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['user__first_name__istartswith',
                     'user__phone', 'user__email']
