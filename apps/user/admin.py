from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address, Staff, Role


admin.site.register([Address, Staff, Role])


class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(User, CustomUserAdmin)
