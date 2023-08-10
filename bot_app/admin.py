import json
import traceback
from typing import Optional

from django.contrib import admin, messages
from django.contrib.admin.widgets import AdminURLFieldWidget
from django.forms import widgets, ModelForm
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from requests import Response

from bot_app.services import *

from .models import *


class PrettyJSONWidget(widgets.Textarea):

    def format_value(self, value):
        try:
            new_value = json.dumps(json.loads(value), indent=2, sort_keys=True, ensure_ascii=False)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in new_value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return new_value
        except Exception as e:
            print(traceback.format_exc())
            return super(PrettyJSONWidget, self).format_value(value)


class ClickableURLFieldWidget(AdminURLFieldWidget):
    def render(self, name, value, attrs=None, renderer=None):
        return mark_safe(f'<a href=\"{value}\" style="padding: 5px 6px">{value}</a>')


class ErrorAdminForm(ModelForm):
    class Meta:
        model = Error
        widgets = {
            'details': PrettyJSONWidget(),
            'traceback_page': ClickableURLFieldWidget()
        }
        fields = '__all__'


# Register your models here.
@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    list_display = ["id", ]
    form = ErrorAdminForm

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["id", "sender", "status"]

@admin.action(description="Запуск рассылку")
def make_published(modeladmin, request, queryset):
    fail_response: Optional[Response] = None
    fail_broadcast: Optional[Broadcast] = None
    for obj in queryset:
        model = obj.get_real_instance_class()
        response = None
        if model is Message:
            response = broadcast_message(obj.get_real_instance())
        elif model is Question:
            response = broadcast_question(obj.get_real_instance())
        elif model is Vote:
            response = publish_vote(obj.get_real_instance())
        elif model is Registry:
            response = publish_registry(obj.get_real_instance())

        if response is not None and not response.ok and fail_response is None:
            fail_response = response
            fail_broadcast = obj

    queryset.update(activated=True)

    if fail_response is not None:
        try:
            data = fail_response.json()
            reason = data['reason']
        except:
            data = None
            reason = None
        messages.error(request, f'{fail_broadcast.name} publish failed. Code: {fail_response.status_code}'
                                f'({fail_response.reason}). '
                                f'{("Reason: " + reason) if reason is not None else ""}')
    else:
        messages.info(request, 'Успех')


class BroadcastChildAdmin(PolymorphicChildModelAdmin):
    base_model = Broadcast
    list_display = ["id", "text", "activated", "response"]
    ordering = ["id", "data"]
    actions = [make_published]


@admin.register(Broadcast)
class BroadcastParentAdmin(PolymorphicParentModelAdmin):
    base_model = Broadcast

    def broadcast_type(self, obj):
        return obj.get_real_instance_class().__name__

    list_display = ["id", "name", "broadcast_type", "response", "activated", ]
    ordering = ["id", "date"]

    child_models = (Question, Vote, Registry, Message)
    list_filter = (PolymorphicChildModelFilter,)
    actions = [make_published]
    polymorphic_list = False


class AnswerAdminInline(admin.TabularInline):
    model = Answer
    extra = 0


class VoteLogAdminInline(admin.TabularInline):
    model = VoteLog
    extra = 0


class RegistryLogAdminInline(admin.TabularInline):
    model = RegistryLog
    extra = 0


class VoteOptionsAdminInline(admin.TabularInline):
    model = VoteOption
    extra = 0


class RegistryEventAdminInline(admin.TabularInline):
    model = RegistryEvent
    extra = 0
    fields = ["id", "text", "max", "count"]


@admin.register(Message)
class AttendanceAdmin(PolymorphicChildModelAdmin):
    base_model = Message


@admin.register(Question)
class AttendanceAdmin(PolymorphicChildModelAdmin):
    base_model = Question
    inlines = [
        AnswerAdminInline,
    ]


@admin.register(Vote)
class AttendanceAdmin(PolymorphicChildModelAdmin):
    base_model = Vote
    inlines = [
        VoteOptionsAdminInline,
        VoteLogAdminInline,
    ]


@admin.register(Registry)
class AttendanceAdmin(PolymorphicChildModelAdmin):
    base_model = Registry
    inlines = [
        RegistryEventAdminInline,
        RegistryLogAdminInline,
    ]


@admin.register(ResponseLog)
class ResponseLogParentAdmin(PolymorphicParentModelAdmin):
    base_model = ResponseLog

    list_display = ["id", "user", "broadcast", ]

    child_models = (RegistryLog,)
    list_filter = (PolymorphicChildModelFilter,)


@admin.register(RegistryLog)
class AttendanceAdmin(PolymorphicChildModelAdmin):
    base_model = RegistryLog
    list_filter = ('broadcast', 'voted_option')
    list_display = ("user", 'broadcast', 'voted_option')


# @admin.register(ResponseLog)
# class ResponseLogAdmin(PolymorphicParentModelAdmin):
#     base_model = ResponseLog
#     child_models = (
#         Answer,
#         Vote,
#         Registry
#     )
#
#     list_display = ('broadcast', 'user')


admin.site.register(VoteOption, )
admin.site.register(RegistryEvent, )


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ["id", ]
