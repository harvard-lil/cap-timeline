from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib import admin
from users.models import TimelineUser


# Register your models here.
class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_verify = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = TimelineUser
        fields = ('email',)

    def clean_password_verification(self):
        password = self.cleaned_data.get("password")
        password_verify = self.cleaned_data.get("password_verify")
        if password and password_verify and password != password_verify:
            raise forms.ValidationError("Passwords don't match")
        return password_verify

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = TimelineUser
        fields = ('email', 'password', 'is_active', )


@admin.register(TimelineUser)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email',)
    list_filter = ('is_staff', )
    fieldsets = (
        (None, {'fields': ('email','timelines')}),
        ('Permissions', {'fields': ('is_staff',)})
    )
    add_fieldsets = (
        (None, {'fields': ('email',)}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
