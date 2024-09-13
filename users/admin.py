from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'name', 'email', 'date_of_birth', 'is_staff', 'is_active')
    ordering = ('name',)
    fieldsets = [
        (
            'Personal Info', {
                'fields': ('name', 'email', 'date_of_birth'),
            }
        ),
        (
            'Login Info', {
                'fields': ('password',),
                'classes': ('collapse',)
            }
        ),
        (
            'Permissions', {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
                'classes': ('collapse',)
            }
        ),
        (
            'Important Dates', {
                'fields': ('last_login', 'date_joined',),
                'classes': ('collapse',)
            }
        )
    ]
