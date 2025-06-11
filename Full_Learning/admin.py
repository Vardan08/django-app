# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
from django.forms import ModelForm

class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'block')
    list_filter = ('is_staff', 'block')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'patronymic', 'registration_address', 'passport_series', 'who_is_passport_from', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Other', {'fields': ('block',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(MyUser, MyUserAdmin)
