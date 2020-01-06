# users/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import TimelineUser


class TimelineUserCreationForm(UserCreationForm):
    class Meta:
        model = TimelineUser
        fields = ('email',)


class TimelineUserChangeForm(UserChangeForm):
    class Meta:
        model = TimelineUser
        fields = ('email',)
