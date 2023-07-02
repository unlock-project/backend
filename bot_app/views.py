import json
from django.shortcuts import render
from django.conf import settings
import requests
from django.http import HttpResponse, JsonResponse


def test(request):
    service = settings.BOT_URL
    url = "api/users/register"
    data = {"username": "1"}
    response = requests.post(service+url, data=json.dumps(data))
    return JsonResponse(response.json())

