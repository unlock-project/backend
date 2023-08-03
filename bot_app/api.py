from typing import List, Optional, Any

import requests
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpRequest
from ninja import NinjaAPI, Schema, Field, File, Form, UploadedFile
from ninja.errors import AuthenticationError
from ninja.responses import Response
from .models import *
from ninja.security import APIKeyQuery
from events_app.models import Attendance, AttendanceLog
from .services import checkinitdata, sendmessage
import datetime

from users_app.models import User


class ApiAuth(APIKeyQuery):
    param_name = 'token'

    def authenticate(self, request: HttpRequest, key: Optional[str]) -> Optional[Any]:
        return (Token.objects.filter(key=key).all()) or request.user.is_staff  # Change to right perms check


apiauth = ApiAuth()

api = NinjaAPI(urls_namespace='botapi')


class CheckInitDataRequest(Schema):
    auth: str = Field(...)


class CheckInitDataResponse(Schema):
    valid: bool = Field(...)
    chat_id: int = Field(...)


class ScannedRequest(Schema):
    auth: str = Field(...)
    qr_data: str = Field(...)
    event_id: int = Field()


class ErrorResponse(Schema):
    reason: str = Field()


# test
class ScannedResponse(Schema):
    first_name: str = Field(...)
    last_name: str = Field(...)
    user_id: int = Field(...)


class ExceptionResponse(Schema):
    error_id: int = Field(...)
    error_url: str = Field(...)


class ExceptionRequest(Schema):
    data: str = Field(...)


class LogsResponse(Schema):
    logs: List[str] = Field(..., example=['log-2023-07-16', 'log-2023-07-14'])


class QRRequest(Schema):
    auth: str = Field(...)


class QRResponse(Schema):
    qr_data: str = Field(...)


class QuestionRequest(Schema):
    question_id: int = Field(...)
    user_id: int = Field(...)
    answer: str = Field(...)


class QuestionResponse(Schema):
    question_id: int = Field(...)
    text: str = Field(...)


class RegistrationRequest(Schema):
    registration_id: int = Field(...)
    user_id: int = Field(...)
    option_id: int = Field(...)


class RegistrationResponse(Schema):
    registration_id: int = Field(...)
    option_id: int = Field(...)
    new_text: str = Field(...)
    message: str = Field(...)


class VoteRequest(Schema):
    vote_id: int = Field(...)
    user_id: int = Field(...)
    option_id: int = Field(...)


class VoteResponse(Schema):
    vote_id: int = Field(...)
    option_id: int = Field(...)
    text: str = Field(...)


class UserIdResponse(Schema):
    user_id: int = Field(..., example=13)


class UserChatIdResponse(Schema):
    chat_id: int = Field(..., example=90284375)


class UserIdRequest(Schema):
    __root__: int = Field(..., example=90284375)


class UserChatIdRequest(Schema):
    __root__: int = Field(..., example=1)


class SendMessageRequest(Schema):
    user_id: int = Field(..., example=123)
    message: str = Field(..., example='Hello world!')


class MessageSentResponse(Schema):
    message: str = Field(..., example='Hello world!')
    message_id: int = Field(..., example=1)


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
    try:
        participant = User.objects.get(qr=qr_data)
    except Exception as ex:
        return 400, ErrorResponse(reason="User with this qr_data not found")

    user = User.objects.get(pk=user_id)
    if not user.is_organizer:
        return 400, ErrorResponse(reason="Unauthorized user")

    attendance = Attendance.objects.get(pk=data.event_id)
    log = AttendanceLog(
        attendance=attendance,
        user=participant,
    )
    log.save()

    sendmessage(participant.id, "Вас отметили")

    return 200, ScannedResponse(user_id=participant.id, first_name=participant.first_name,
                                last_name=participant.last_name)


@api.post("/error", response=ExceptionResponse, auth=apiauth)
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


@api.get("/logs", response={200: LogsResponse, 500: ErrorResponse}, auth=apiauth)
def logs_request(request: WSGIRequest):
    try:
        logs = requests.get(settings.BOT_URL + '/logs').json()["logs"]
    except Exception as ex:
        return 500, ErrorResponse(reason=str(ex.args))
    return 200, LogsResponse(logs=logs)


@api.get("/user/id", response={200: UserIdResponse, 400: ErrorResponse}, auth=apiauth)
def user_id_request(request: WSGIRequest, chat_id: int):
    try:
        response = requests.get(settings.BOT_URL + '/user/id', params={'chat_id': chat_id})
        data = response.json()

        if not response.ok:
            return 400, ErrorResponse(**data)
        user_id = data['user_id']
    except Exception as ex:
        return 400, ErrorResponse(reason=str(ex))
    return 200, UserIdResponse(user_id=user_id)


@api.get("/user/chat-id", response={200: UserChatIdResponse, 400: ErrorResponse}, auth=apiauth)
def user_id_request(request: WSGIRequest, user_id: int):
    try:
        response = requests.get(settings.BOT_URL + '/user/chat-id', params={'user_id': user_id})
        data = response.json()
        if not response.ok:
            return 400, ErrorResponse(**data)
        chat_id = data['chat_id']
    except Exception as ex:
        return 400, ErrorResponse(reason=str(ex))
    return 200, UserChatIdResponse(chat_id=chat_id)


@api.post("/user/message", response={200: MessageSentResponse, 400: ErrorResponse}, auth=apiauth)
def send_msg_request(request: WSGIRequest, data: SendMessageRequest):
    try:
        result = sendmessage(data.user_id, data.message)
        data = result.json()
        if not result.ok:
            return 400, ErrorResponse(**data)
    except Exception as ex:
        return 400, ErrorResponse(reason=str(ex))
    return 200, MessageSentResponse(**data)


@api.post("/qr", response={200: QRResponse, 400: ErrorResponse})
def qr_request(request: WSGIRequest, data: QRRequest):
    checked_data = checkinitdata(data.auth)
    if 'valid' not in checked_data.keys() or not checked_data['valid'] or 'chat_id' not in checked_data.keys():
        return 400, ErrorResponse(reason="Not valid telegram web app data")

    chat_id = checked_data["chat_id"]
    try:
        user_id = requests.get(settings.BOT_URL + '/user/id', params={'chat_id': chat_id}).json()["user_id"]  # User who
        user = User.objects.get(id=user_id)
        qr_data = user.qr
    except Exception as ex:
        return 400, ErrorResponse(reason=ex.args)

    if not qr_data:
        return 400, ErrorResponse(reason="No qr data")

    return QRResponse(qr_data=qr_data)


@api.post("/question/response", response={200: QuestionResponse, 400: ErrorResponse})
def answer_request(request: WSGIRequest, data: QuestionRequest):
    try:
        question = Question.objects.get(pk=data.question_id)
        message = question.response
    except Exception as ex:
        return 400, ErrorResponse(reason=ex.args[0])

    try:
        answer = Answer(
            time=datetime.datetime.now(),
            date=datetime.date.today(),
            user=User.objects.get(pk=data.user_id),
            broadcast=question,
            text=data.answer
        )
        answer.save()

    except Exception as ex:
        return 400, ErrorResponse(reason=ex.args)

    return 200, QuestionResponse(question_id=data.question_id, text=message)


@api.post("/registration/response", response={200: RegistrationResponse, 400: ErrorResponse})
def event_register_request(request: WSGIRequest, data: RegistrationRequest):
    try:
        registration = Registry.objects.get(pk=data.registration_id)
    except Exception as ex:
        return 400, ErrorResponse(reason=ex.args[0])

    try:
        registration_event = RegistryEvent.objects.get(pk=data.option_id)

        if registration_event.max <= registration_event.count:
            return 200, RegistrationResponse(registration_id=data.registration_id, option_id=data.option_id,
                                             new_text=registration_event.bot_text,
                                             message=registration_event.full_message)

        message = registration_event.success_message

    except Exception as ex:
        return 400, ErrorResponse(reason=ex.args[0])

    logs = RegistryLog.objects.filter(user=User.objects.get(pk=data.user_id), broadcast=registration)

    if logs.exists():
        return 200, RegistrationResponse(registration_id=data.registration_id, option_id=data.option_id,
                                         new_text=registration_event.bot_text, message=registration_event.error_message)
    try:
        registry = RegistryLog(
            time=datetime.datetime.now(),
            date=datetime.date.today(),
            user=User.objects.get(pk=data.user_id),
            broadcast=registration,
            voted_option=registration_event
        )
        registry.save()

        registration_event = RegistryEvent.objects.get(pk=registration_event.id)
    except Exception as ex:
        return 400, ErrorResponse(reason=ex.args)

    return 200, RegistrationResponse(registration_id=data.registration_id, option_id=data.option_id,
                                     new_text=registration_event.bot_text, message=message)


@api.post("/vote/response", response={200: VoteResponse, 400: ErrorResponse})
def choose_request(request: WSGIRequest, data: VoteRequest):
    try:
        vote = Vote.objects.get(pk=data.vote_id)
    except Exception as ex:
        return 400, ErrorResponse(reason=ex.args[0])

    try:
        user = User.objects.get(pk=data.user_id)
    except Exception as ex:
        return 400, ErrorResponse(reason=ex.args[0])

    try:
        vote_option = VoteOption.objects.get(pk=data.option_id)

        if vote_option.team == user.team:
            return 200, VoteResponse(vote_id=data.vote_id, option_id=data.option_id,
                                     text=vote.same_team_message)

        message = vote.success_message

    except Exception as ex:
        return 400, ErrorResponse(reason=ex.args[0])

    logs = VoteLog.objects.filter(user=User.objects.get(pk=data.user_id), broadcast=vote)

    if logs.exists():
        return 200, VoteResponse(vote_id=data.vote_id, option_id=data.option_id,
                                 text=vote.error_message)
    try:
        registry = VoteLog(
            time=datetime.datetime.now(),
            date=datetime.date.today(),
            user=User.objects.get(pk=data.user_id),
            broadcast=vote,
            voted_option=vote_option
        )
        registry.save()

    except Exception as ex:
        return 400, ErrorResponse(reason=ex.args)

    return 200, VoteResponse(vote_id=data.vote_id, option_id=data.option_id,
                             text=message)


@api.exception_handler(AuthenticationError)
def unauthorizedError(request, exc):
    return api.create_response(request, {'reason': 'Unauthorized'}, status=401)
