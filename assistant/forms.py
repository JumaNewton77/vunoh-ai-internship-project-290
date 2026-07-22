from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Django's built-in UserCreationForm validates against auth.User by
    default. Since AUTH_USER_MODEL is swapped to assistant.CustomUser
    in settings.py, using the stock form crashes on submit with:
        AttributeError: Manager isn't available;
        'auth.User' has been swapped for 'assistant.CustomUser'
    Pointing Meta.model at CustomUser fixes it.
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username",)