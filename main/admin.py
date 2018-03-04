# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.forms import MyUserChangeForm, MyUserCreationForm
from .models import MyUser, Activation, Feedback


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm

    list_display = (
        'email',
        'name',
        'is_active',
        'is_admin',
        'timestamp',
    )

    list_filter = ('is_admin', 'is_active',)

    search_fields = ('email', 'name')

    ordering = ('-timestamp',)

    fieldsets = (
        (None, {'fields': (
                    'email',
                    'name',
                    'push_token',
                    'sound',
                    'tariff',
                    'tariff_date'
            )}),
        ('Password', {'fields': ('password', )}),  # we can change password in admin-site
        ('Permissions', {'fields': ('is_active', 'is_admin')})
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'name', 'password1', 'password2', 'tariff', 'tariff_date')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', ) }),
    )


@admin.register(Activation)
class ActivationAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'used')

    list_filter = ('used',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp')
