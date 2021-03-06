from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models

# Register your models here.


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    '''Admin View for User'''
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Personal Info'), {
            'fields': ('name',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        (_('Important dates'), {
            'fields': ('last_login',)
        }),
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    readonly_fields = ('id',)
    search_fields = ('name', 'email')
