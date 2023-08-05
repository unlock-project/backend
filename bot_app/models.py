import os
import secrets

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver
from polymorphic.models import PolymorphicModel

from events_app.models import Event
from users_app.models import User, Team


def generateKey():
    return secrets.token_hex(16)


# Create your models here.
class Broadcast(PolymorphicModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    time = models.TimeField(auto_now=False, null=True, blank=True)
    date = models.DateField(auto_now=False, null=True, blank=True)
    users = models.ManyToManyField(to=User, related_name='users_list', default=User.all_users)
    response = models.TextField(max_length=100, blank=True, null=True, default="Ответ получен, спасибо!")
    activated = models.BooleanField(default=False, )

    def __str__(self):
        return f"{str(self.date)} {self.name}"


class Message(Broadcast):
    text = models.TextField(max_length=400, blank=True, null=True)


class Question(Broadcast):
    text = models.TextField(max_length=400)


class Error(models.Model):
    id = models.AutoField(primary_key=True)
    details = models.TextField()
    traceback_page = models.URLField()


@receiver(post_delete, sender=Error)
def _error_delete(sender, instance: Error, **kwargs):
    expected_path = settings.TEMPLATES[0]['DIRS'][0] / "tracebacks" / f"error{instance.id}.html"
    if expected_path.exists():
        os.remove(expected_path)


class Vote(Broadcast):
    text = models.TextField(max_length=400)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, null=True, blank=True)
    close_time = models.TimeField(auto_now=False, null=True, blank=True)

    @property
    def success_message(self):
        return f"Спасибо за выбор!"

    @property
    def error_message(self):
        return f"Ты уже проголосовал."

    @property
    def same_team_message(self):
        return f"Ты не можешь за свою команду голосовать."


class VoteOption(models.Model):
    text = models.TextField(max_length=100)
    voting = models.ForeignKey(Vote, related_name='vote_options', on_delete=models.CASCADE, null=False)
    count = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        text = self.text
        if len(text) > 15:
            return text[:15] + "..."
        return text


class Registry(Broadcast):
    text = models.TextField(max_length=500)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, null=True, blank=True)


class Token(models.Model):
    key = models.CharField(max_length=50, default=generateKey, unique=True)


class RegistryEvent(models.Model):
    text = models.TextField(max_length=100)
    count = models.IntegerField(default=0)
    max = models.IntegerField(null=True, blank=True)
    registry = models.ForeignKey(Registry, related_name='options', on_delete=models.CASCADE, null=False)

    @property
    def bot_text(self):
        return f"{self.text} ({self.count}/{self.max})"

    @property
    def success_message(self):
        return f"Ты зарегистрировался на {self.text}"

    @property
    def error_message(self):
        return f"Ты уже зарегистрировался"

    @property
    def full_message(self):
        return f"К сожалению, уже нет мест на данном ивенте"

    def __str__(self):
        text = self.text
        if len(text) > 15:
            return text[:15] + "..."
        return f"{str(self.registry)} | {text}"


class ResponseLog(PolymorphicModel):
    time = models.TimeField(auto_now=False, null=True, blank=True)
    date = models.DateField(auto_now=False, null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    broadcast = None

    def __str__(self):
        return f"{str(self.broadcast)} {str(self.user)}"


class Answer(ResponseLog):
    broadcast = models.ForeignKey(to=Question, on_delete=models.DO_NOTHING, )
    text = models.TextField(max_length=400)


class VoteLog(ResponseLog):
    broadcast = models.ForeignKey(to=Vote, on_delete=models.DO_NOTHING, )
    voted_option = models.ForeignKey(to=VoteOption,
                                     on_delete=models.DO_NOTHING, )


@receiver(post_save, sender=VoteLog)
def _register_to_event(sender, instance: VoteLog, **kwargs):
    vote_option = VoteOption.objects.get(pk=instance.voted_option.id)
    vote_option.count += 1
    vote_option.save()


@receiver(post_delete, sender=VoteLog)
def _cancel_register(sender, instance: VoteLog, **kwargs):
    vote_option = VoteOption.objects.get(pk=instance.voted_option.id)
    vote_option.count -= 1
    vote_option.save()


class RegistryLog(ResponseLog):
    broadcast = models.ForeignKey(to=Registry, on_delete=models.DO_NOTHING, )
    voted_option = models.ForeignKey(to=RegistryEvent,
                                     on_delete=models.DO_NOTHING, )


@receiver(post_save, sender=RegistryLog)
def _register_to_event(sender, instance: RegistryLog, **kwargs):
    registration_event = RegistryEvent.objects.get(pk=instance.voted_option.id)
    registration_event.count += 1
    registration_event.save()


@receiver(post_delete, sender=RegistryLog)
def _cancel_register(sender, instance: RegistryLog, **kwargs):
    registration_event = RegistryEvent.objects.get(pk=instance.voted_option.id)
    registration_event.count -= 1
    registration_event.save()
