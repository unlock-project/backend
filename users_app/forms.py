from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "balance",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "balance",)
