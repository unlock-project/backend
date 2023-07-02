import json
from django.shortcuts import render
from django.conf import settings
import requests
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from .services import checkinitdata




def test(request):
    service = settings.BOT_URL
    url = "api/users/register"
    data = {"username": "1"}
    response = requests.post(service + url, data=json.dumps(data))
    return JsonResponse(response.json())


@csrf_exempt
def api_checkinitdata(request):
    if request.method == "POST":
        service = settings.BOT_URL
        response = requests.get(service + '/user/validate', params={'_auth': json.loads(request.body)['_auth']})
        return JsonResponse(response.json())
    else:
        raise Http404()


@csrf_exempt
def api_scanned(request):
    if request.method == "POST":
        service = settings.BOT_URL
        data = json.loads(request.body)
        checked_data = checkinitdata(data["_auth"])
        if 'valid' not in checked_data.keys() or not checked_data['valid']:
            return JsonResponse({'reason': 'Not valid telegram web app data'})
        chat_id = checked_data["chat_id"]
        user_id = requests.get(service + '/user/id', params={'chat_id': chat_id}).json()["user_id"]
        qr_data = data['qr_data']
        # CHECK IF USER IS ORGANIZER
        # DO MAGIC

        return JsonResponse({'YOU': {'user_id': user_id, 'chat_id': chat_id}, 'QR': qr_data})
    else:
        raise Http404()


def qrscanner_page(request):
    return render(request, "qrscanner/index.html")
