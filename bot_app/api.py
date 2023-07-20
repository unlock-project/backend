from typing import List

import requests
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from ninja import NinjaAPI, Schema, Field, File, Form, UploadedFile
from ninja.responses import Response

from .models import Error
from .services import checkinitdata

api = NinjaAPI(urls_namespace='botapi')


class CheckInitDataRequest(Schema):
    auth: str = Field(...)


class CheckInitDataResponse(Schema):
    valid: bool = Field(...)
    chat_id: int = Field(...)


class ScannedRequest(Schema):
    auth: str = Field(...)
    qr_data: str = Field(...)


class ErrorResponse(Schema):
    reason: str = Field()


# test
class ScannedResponse(Schema):
    user_id: int = Field(...)
    qr_data: str = Field(...)


class ExceptionResponse(Schema):
    error_id: int = Field(...)
    error_url: str = Field(...)


class ExceptionRequest(Schema):
    data: str = Field(...)

class LogsResponse(Schema):
    logs: List[str] = Field(..., example=['log-2023-07-16', 'log-2023-07-14'])

@api.post("/checkinitdata", response=CheckInitDataResponse)
def checkinitdata_request(request, data: CheckInitDataRequest):
    response = checkinitdata(data.auth)
    return CheckInitDataResponse(**response)


@api.post("/scanned", response={200: ScannedResponse, 400: ErrorResponse})
def scanned_request(request, data: ScannedRequest):
    checked_data = checkinitdata(data.auth)
    if 'valid' not in checked_data.keys() or not checked_data['valid'] or 'chat_id' not in checked_data.keys():
        return 400, ErrorResponse(reason="Not valid telegram web app data")
    chat_id = checked_data["chat_id"]  # User who scanned qr code
    try:
        user_id = requests.get(settings.BOT_URL + '/user/id', params={'chat_id': chat_id}).json()["user_id"]  # User who
    except Exception as ex:
        return 400, ErrorResponse(reason=ex.args)
    # scanned qr code
    qr_data = data.qr_data
    # CHECK IF USER IS ORGANIZER
    # DO MAGIC
    return 200, ScannedResponse(user_id=user_id, qr_data=qr_data)


@api.post("/error", response=ExceptionResponse)
def error_request(request: WSGIRequest, data: ExceptionRequest = Form(...), traceback: UploadedFile = File(...)):
    template_dir = settings.TEMPLATES[0]['DIRS'][0]
    error_model = Error(details=data.data, traceback_page="")
    error_model.save()
    error_id = error_model.id
    with open(template_dir / "tracebacks" / f"error{error_id}.html", "wb") as file:
        file.write(traceback.read())
        error_model.traceback_page = f"/bot/error/{error_id}/"
        error_model.save()
    return ExceptionResponse(error_id=error_id, error_url=error_model.traceback_page)

@api.get("/logs", response={200: LogsResponse, 500: ErrorResponse})
def logs_request(request: WSGIRequest):
    try:
        logs = requests.get(settings.BOT_URL + '/logs').json()["logs"]
    except Exception as ex:
        return 500, ErrorResponse(reason=str(ex.args))
    return 200, LogsResponse(logs=logs)
