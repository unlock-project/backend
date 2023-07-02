from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from bot_app.models import *
from bot_app.services import *


@admin.action(description="Запуск рассылку")
def make_published(modeladmin, request, queryset):
    for obj in queryset:
        model = obj.get_real_instance_class()
        if model is Message:

            broadcast_message(obj.get_real_instance())
        elif model is Vote:
            publish_vote(obj.get_real_instance())
        elif model is Registry:
            publish_registry(obj.get_real_instance())

    queryset.update(activated=True)


class BroadcastChildAdmin(PolymorphicChildModelAdmin):
    base_model = Broadcast
    list_display = ["id", "text", "activated"]
    ordering = ["id"]
    actions = [make_published]


@admin.register(Broadcast)
class BroadcastParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = Broadcast
    list_display = ["id", "name", "activated"]
    child_models = (Question, Vote, Registry)
    list_filter = (PolymorphicChildModelFilter,)
    actions = [make_published]


admin.site.register(Question, BroadcastChildAdmin)
admin.site.register(Vote, )
admin.site.register(VoteOption, )
admin.site.register(Registry, )
admin.site.register(RegistryEvent, )
