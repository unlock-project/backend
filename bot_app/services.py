import json
import requests
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Message, Question, Vote, VoteOption, Registry, RegistryEvent, Report


def broadcast_message(message: Message):
    service = settings.BOT_URL + "/message/publish"
    data = {
        "message_id": message.id,
        "message_text": message.text,
    }
    response = requests.post(service, json=data)
    return response


def broadcast_question(question: Question):
    service = settings.BOT_URL + "/question/publish"
    data = {
        "question_id": question.id,
        "question_text": question.text,
    }
    json_data = json.dumps(data)
    response = requests.post(service, json=data)
    return response


def publish_vote(vote: Vote):
    service = settings.BOT_URL + "/vote/publish"
    options = VoteOption.objects.filter(voting__id=vote.id)
    options_serial = []
    for option in options:
        options_serial.append({
            "option_id": option.id,
            "option_text": option.text,
        })

    data = {
        "vote_id": vote.id,
        "vote_text": vote.text,
        "options": options_serial,
    }
    response = requests.post(service, json=data)
    return response


def publish_registry(registry: Registry):
    service = settings.BOT_URL + "/registration/publish"
    events = RegistryEvent.objects.filter(registry_id=registry.id)
    options = []
    for event in events:
        options.append({
            "option_id": event.id,
            "option_text": event.bot_text,
        })

    data = {
        "registration_id": registry.id,
        "registration_text": registry.text,
        "options": options,
    }

    response = requests.post(service, json=data)
    return response


def update_registry(registry: Registry):
    service = settings.BOT_URL + "/registration/update"
    events = RegistryEvent.objects.filter(registry_id=registry.id)
    options = []
    for event in events:
        options.append({
            "option_id": event.id,
            "option_text": event.bot_text,
        })

    data = {
        "registration_id": registry.id,
        "registration_text": registry.text,
        "options": options,
    }

    response = requests.post(service, json=data)
    return response


def checkinitdata(_auth: str) -> dict:
    service = settings.BOT_URL
    response = requests.get(service + '/user/validate', params={'auth': _auth})
    result = json.loads(response.content)
    return result


def sendmessage(user_id: int, message: str):
    data = json.dumps({"user_id": user_id, "message": message})
    response = requests.post(settings.BOT_URL + '/sendmessage',
                             data=data,
                             headers={"content-type": "application/json", })
    return response


@receiver(pre_save, sender=Report)
def _report_update(sender: Report, instance: Report, **kwargs):
    try:
        old_instance = Report.objects.get(id=instance.id)
    except Report.DoesNotExist:
        return
    if old_instance.status != instance.status:
        new_status_label = instance.ReportStatus(instance.status).label
        sendmessage(instance.sender.id, f'Статус вашего обращения с номером <i><b>{instance.id}</b></i> изменился на <i><b>{new_status_label}</b></i>')