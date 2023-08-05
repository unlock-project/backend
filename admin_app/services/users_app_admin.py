from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users_app.forms import CustomUserCreationForm, CustomUserChangeForm
from users_app.models import *
from events_app.admin import ContestAdminInline, AttendanceAdminInline


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("last_name", "first_name", "telegram", "team","is_organizer", "is_staff")
    list_editable = ("is_organizer", "is_staff")
    list_filter = ("team", "is_organizer",)
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
    search_fields = ("last_name", "telegram")
    ordering = ("username",)
    inlines = [
        AttendanceAdminInline,
    ]


admin.site.register(User, CustomUserAdmin)


@admin.register(Team)
class AttendanceAdmin(admin.ModelAdmin):
    model = Team
    list_display = ('id', 'name', 'balance', 'tutor')
    inlines = [
        ContestAdminInline,
    ]
