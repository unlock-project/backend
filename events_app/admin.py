from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter

from django.db.models.signals import pre_save
from .models import *


class ContestAdminInline(admin.TabularInline):
    model = ContestLog
    extra = 0


class BonusTeamAdminInline(admin.TabularInline):
    model = BonusTeamLog
    extra = 0


class BonusUserAdminInline(admin.TabularInline):
    model = BonusUserLog
    extra = 0


class AttendanceAdminInline(admin.TabularInline):
    model = AttendanceLog
    extra = 0


@admin.register(Event)
class EventAdmin(PolymorphicParentModelAdmin):
    model = Event
    list_filter = (PolymorphicChildModelFilter,)
    child_models = (
        Attendance,
        Contest,
        BonusTeam,
        BonusUser,
        Promo,
    )

    def event_type(self, obj):
        return obj.get_real_instance_class().__name__

    list_display = ('name', 'event_type', )


@admin.register(Attendance)
class AttendanceAdmin(PolymorphicChildModelAdmin):
    base_model = Attendance
    inlines = [
        AttendanceAdminInline,
    ]


@admin.register(Contest)
class ContestAdmin(PolymorphicChildModelAdmin):
    base_model = Contest
    inlines = [
        ContestAdminInline,
    ]


@admin.register(BonusTeam)
class BonusTeamAdmin(PolymorphicChildModelAdmin):
    base_model = BonusTeam
    inlines = [
        BonusTeamAdminInline,
    ]
    pass


@admin.register(BonusUser)
class BonusUserAdmin(PolymorphicChildModelAdmin):
    base_model = BonusUser
    inlines = [
        BonusUserAdminInline,
    ]
    pass


@admin.register(Promo)
class PromoAdmin(PolymorphicChildModelAdmin):
    base_model = Promo
    list_display = ('name', 'promo_code', 'condition', 'code_type', 'used_by', 'score', )
    pass




