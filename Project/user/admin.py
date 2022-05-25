from email import message
from pyexpat import model
from pyexpat.errors import messages
from tabnanny import verbose
from weakref import proxy
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Chapter, Professor, User,Student, Professor_Student, Group, Professor_Level, Request
from django.contrib import messages
from rest_framework_simplejwt.token_blacklist.admin import BlacklistedToken,OutstandingToken
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)

class ProfessorRequest(User):
    class Meta : 
        proxy = True

class StudentsList(User):
    class Meta : 
        proxy = True

class ProfessorList(User):
    class Meta:
        proxy=True

class ProfessorLine (admin.StackedInline):
    model = Professor
class StudentLine (admin.StackedInline):
    model = Student

@admin.register(StudentsList)
class StudentsList(admin.ModelAdmin):
    inlines = [StudentLine]
    search_fields = ['email', 'phone', 'student_name']
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    fieldsets = (
        (None, {'fields': (('first_name', 'last_name'),'password', 'email', 'phone', 'role')}),
        ('Permissions', {
            'fields': ('is_active', 'is_superuser', 'is_staff',)}),
        ('Time', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    def get_queryset(self, request):
        qs = super(StudentsList, self).get_queryset(request)
        return qs.filter(role='S')
@admin.register(ProfessorRequest)
class ProfessorRequest(admin.ModelAdmin):
    list_display = ['professor_name','email', 'phone', 'is_active']
    search_fields = ['email', 'phone', 'student_name']
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    ordering = ['email']
    fieldsets = (
        (None, {'fields': (('first_name', 'last_name'),'password', 'email', 'phone', 'role')}),
        ('Permissions', {
            'fields': ('is_active', 'is_superuser', 'is_staff',)}),
        ('Time', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    def make_active (modeladmin,request, queryset):
        queryset.update(is_active = True)
        messages.success(request , "Selected Record(s) Marked as Active Successfully !!")
    def make_inactive (modeladmin,request, queryset):
        queryset.update(is_active = False)
        messages.success(request , "Selected Record(s) Marked as Inactive Successfully !!")
    def get_queryset(self, request):
        qs = super(ProfessorRequest, self).get_queryset(request)
        return qs.filter(is_active = False, role='P')
    def professor_name(self, object):
        return f'{object.first_name} {object.last_name}'
    admin.site.add_action(make_active, "Make Active")
    admin.site.add_action(make_inactive, "Make Inactive")

@admin.register(ProfessorList)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [ProfessorLine]
    def get_queryset(self, request):
        qs = super(CustomUserAdmin, self).get_queryset(request)
        return qs.filter(is_active = True, role='P')
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = Professor
    list_display = ['user_name', 'email', 'phone', 'is_active']
    list_display_links = ('user_name', 'email',)
    search_fields = ['email', 'phone', 'first_name' ]
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

#@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['professor_name', 'email', 'phone']
    list_display_links = ('professor_name', 'email',)
    list_per_page = 20
    list_select_related = ['user']
    ordering = ['user__email']
    @admin.display(description='Professor name')
    def professor_name(self, object):
        return f'{object.user.first_name} {object.user.last_name}'


# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ['student_name', 'email', 'phone']
#     list_display_links = ('student_name','email')
#     list_per_page = 20
#     list_select_related = ['user']
#     ordering = ['user_first_name', 'user_last_name']
#     search_fields = ['user_first_name_istartswith',
#                     'user_phone', 'user_email']

#     @admin.display(description='Student name')
#     def student_name(self, object):
#         return f'{object.user.first_name} {object.user.last_name}'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['professor_name', 'name', 'level', 'created_at']
    list_per_page = 20
    @admin.display(description='Professor name')
    def professor_name(self, object):
        return f'{object.professor.user.first_name} {object.professor.user.last_name}'

@admin.register(Professor_Student)
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

@admin.register(Professor_Level)
class ProfessorLevelAdmin(admin.ModelAdmin):
    list_display = ['professor_name', 'level']
    readonly_fields = ('score')
    list_per_page = 20
    ordering = ['level']
    @admin.display(description='Professor name')
    def professor_name(self, object):
        return f'{object.professor.user.first_name} {object.professor.user.last_name}'