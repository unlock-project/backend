from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users_app.forms import CustomUserCreationForm, CustomUserChangeForm
from users_app.models import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("username", "telegram", "is_staff", "is_active",)
    list_filter = ("username", "telegram", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "team", "balance", "telegram", "qr")}),
        ("Permissions", {"fields": ("is_organizer", "is_staff", "is_active", "groups", "user_permissions")}),

    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "first_name", "last_name", "telegram", "qr", "password1", "password2",
                "is_organizer", "is_staff", "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("username", "telegram")
    ordering = ("username",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Team, )
