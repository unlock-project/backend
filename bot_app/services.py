import json

import requests
from django.conf import settings

from .models import Message, Vote, VoteOption, Registry, RegistryEvent


def broadcast_message(message: Message):
    service = settings.BOT_URL + "/message/publish"
    data = {
        "message_id": message.id,
        "message_text": message.text,
    }
    response = requests.post(service, data=json.dumps(data))
    return response.json()


def publish_vote(vote: Vote):
    service = settings.BOT_URL + "/vote/publish"
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
    service = settings.BOT_URL + "/registry/publish"
    events = RegistryEvent.objects.filter(registry_id=registry.id)
    options = []
    for event in events:
        options.append(event.bot_text)

    data = {
        "event_id": registry.event.id if registry.event is not None else None,
        "text": registry.text,
        "options": options,
    }


def checkinitdata(_auth: str) -> dict:
    service = settings.BOT_URL
    response = requests.get(service + '/user/validate', params={'auth': _auth})
    result = json.loads(response.content)
    return result

def sendmessage(user_id: int, message:str):
    data = json.dumps({"user_id": user_id, "message": message})
    response = requests.post(settings.BOT_URL + '/sendmessage',
                            data=data,
                            headers={"content-type": "application/json", })
    return response.ok