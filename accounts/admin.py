from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.forms import StoreStackUserForm, StoreStackUserChangeForm
from accounts.models import StoreStackUser


@admin.register(StoreStackUser)
class StoreStackUserAdmin(UserAdmin):
    form = StoreStackUserChangeForm
    add_form = StoreStackUserForm

    list_display = ['username', 'email', 'user_type', 'is_staff', 'is_active']
    list_filter = ['user_type', 'is_staff', 'is_active', 'is_superuser']
    search_fields = ['username', 'email']
    ordering = ['username']
    readonly_fields = ['last_login', 'date_joined']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('User Type', {'fields': ('user_type',)}),
    )
