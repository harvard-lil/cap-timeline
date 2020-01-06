# from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from users.models import TimelineUser
from users import forms


class UserAdmin(BaseUserAdmin):
    form = forms.TimelineUserChangeForm
    add_form = forms.TimelineUserCreationForm

    list_display = ('email',)
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'timelines', 'password')}),
        ('Permissions', {'fields': ('is_staff',)})
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password', 'password2', 'is_staff', 'is_superuser')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(TimelineUser, UserAdmin)
