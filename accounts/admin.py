from django.contrib import admin

from accounts.models import StoreStackUser


@admin.register(StoreStackUser)
class StoreStackUserAdmin(admin.ModelAdmin):
        list_display = ['username', 'email', 'user_type', 'is_staff', 'is_active', 'date_joined']
        list_filter = ['user_type', 'is_staff', 'is_active']
        search_fields = ['username', 'email']
        ordering = ['username']

        fieldsets = (
            (None, {'fields': ('username', 'password')}),
            ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
            ('Important dates', {'fields': ('last_login', 'date_joined')}),
            ('User Type', {'fields': ('user_type',)}),
        )
        add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2', 'user_type'),
            }),
        )
