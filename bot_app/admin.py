import json
import traceback

from django.contrib import admin
from django.contrib.admin.widgets import AdminURLFieldWidget
from django.forms import widgets, ModelForm
from django.utils.safestring import mark_safe
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
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


@admin.action(description="Запуск рассылку")
def make_published(modeladmin, request, queryset):
    for obj in queryset:
        model = obj.get_real_instance_class()
        if model is Message:
            broadcast_message(obj.get_real_instance())
        elif model is Question:
            broadcast_question(obj.get_real_instance())
        elif model is Vote:
            publish_vote(obj.get_real_instance())
        elif model is Registry:
            publish_registry(obj.get_real_instance())

    queryset.update(activated=True)


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
