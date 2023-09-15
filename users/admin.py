from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'name', 'email', 'date_of_birth', 'is_staff', 'is_active')
    ordering = ('name',)
