from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models


class UserAdmin(BaseUserAdmin):
    """
    This our custom user admin.
    """
    ordering = ['id']
    list_display = ['email', 'name']


# Now we need to register our UserAdmin class
admin.site.register(models.User, UserAdmin)