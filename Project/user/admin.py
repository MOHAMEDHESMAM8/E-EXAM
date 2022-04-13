from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User 


admin.site.unregister(Group)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = User

    list_display = ['first_name','last_name','email', 'phone', 'role', 'is_active']
    search_fields = ['email', 'phone', 'first_name']
    list_filter = ['is_active']
    
    readonly_fields = ('created_at', 'updated_at', 'last_login')

    fieldsets = (
        (None, {'fields': (('first_name', 'last_name'), 'password', 'email', 'phone','role')}),
        ('Permissions', {'fields': ('is_active','is_superuser','is_staff',)}),
        ('Time', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name','email', 'phone','password','password_2','role')}),
    )

    ordering = ['email']
    filter_horizontal = ()


