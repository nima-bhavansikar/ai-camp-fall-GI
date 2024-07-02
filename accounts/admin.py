from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserData, CustomUser
# Register your models here.

admin.site.register(UserData)

class CustomUserAdmin(UserAdmin):
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)