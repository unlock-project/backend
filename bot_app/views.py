import json

import requests
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render
from .models import Error


def test(request):
    service = settings.BOT_URL
    url = "api/users/register"
    data = {"username": "1"}
    response = requests.post(service + url, data=json.dumps(data))
    return JsonResponse(response.json())


def qrscanner_page(request):
    return render(request, "qrscanner/index.html")


def has_access_to_traceback(user) -> bool:
    #  add there permissions checking (function should return bool)
    return user.is_staff


@user_passes_test(has_access_to_traceback)
def error_page(request, error_id):
    if Error.objects.filter(id=error_id).exists():
        return render(request, f"tracebacks/error{error_id}.html")
    raise Http404()

@user_passes_test(has_access_to_traceback)
def specific_log(request, filename):
    try:
        response = requests.get(settings.BOT_URL + f'/logs/{filename}')
    except Exception as ex:
        raise Http404()
    if not response.ok:
        raise Http404()

    return HttpResponse(response.content, status=200, content_type="text/plain")