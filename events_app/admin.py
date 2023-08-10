import json

from django.contrib import admin
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpRequest
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter

from django.db.models.signals import pre_save
from .models import *


class ContestAdminInline(admin.TabularInline):
    model = ContestLog
    # readonly_fields = ["team", "score"]

    extra = 0



class BonusTeamAdminInline(admin.TabularInline):
    model = BonusTeamLog
    extra = 0


class BonusUserAdminInline(admin.TabularInline):
    model = BonusUserLog
    extra = 0


class AttendanceAdminInline(admin.TabularInline):
    model = AttendanceLog
    # readonly_fields = ['user', 'team']

    extra = 0


@admin.register(Event)
class EventAdmin(PolymorphicParentModelAdmin):
    model = Event
    list_filter = (PolymorphicChildModelFilter, 'date',)
    child_models = (
        Attendance,
        Contest,
        Promo,
    )

    def event_type(self, obj):
        return obj.get_real_instance_class().__name__

    list_display = ('name', 'event_type', )


@admin.register(Attendance)
class AttendanceAdmin(PolymorphicChildModelAdmin):
    base_model = Attendance
    list_display = ('id', 'name', 'score')
    # list_editable = ('score',)
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
    add_form_template = 'promo/change_form.html'

    def response_add(self, request: HttpRequest, obj: Promo, post_url_continue=None):
        if "_add_bulk" in request.POST:
            count_s = request.POST.get('count', 1)
            count = int(count_s if count_s else '1')

            for i in range(2, count+1):
                for _ in range(5):
                    try:
                        n_promo = Promo(code_type=obj.code_type, score=obj.score,
                                        message=obj.message, name=f'{obj.name}_{i}',
                                        used_by=obj.used_by, condition=obj.condition)
                        n_promo.save()
                        break
                    except IntegrityError as ex:
                        pass
                    except:
                        break

            obj.name = f'{obj.name}_1'
            obj.save()

            return HttpResponseRedirect("..")

        else:
            return super().response_add(request, obj, post_url_continue)




