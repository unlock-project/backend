import json
from microservice_request.services import ConnectionService
import requests
from django.conf import settings
from .models import Message, Vote, VoteOption, Registry, RegistryEvent
from django.core import serializers


def broadcast_message(message: Message):
    service = settings.BOT_URL+"/message/publish"
    data = {
            "message_id": message.id,
            "message_text": message.text,
        }
    response = requests.post(service, data=json.dumps(data))
    return response.json()


def publish_vote(vote: Vote):
    service = settings.BOT_URL+"/vote/publish"
    options = VoteOption.objects.filter(voting__id=vote.id)
    options_serial = []
    for option in options:
        options.append({
            "id": option.id,
            "text": option.text,
        })

    data = {
            "vote_id": vote.id,
            "vote_text": vote.text,
            "options": options,
        }
    response = requests.post(service, data=json.dumps(data))
    return response.json()


def publish_registry(registry: Registry):
    service = settings.BOT_URL+"/registry/publish"
    events = RegistryEvent.objects.filter(registry_id=registry.id)
    options = []
    for event in events:
        options.append(event.bot_text)

    data = {
        "event_id": registry.event.id if registry.event is not None else None,
        "text": registry.text,
        "options": options,
    }

    response = requests.post(service, data=json.dumps(data))
    return response.json()


Ц
