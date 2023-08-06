from ninja import NinjaAPI, Schema, Field, File, Form, UploadedFile

from bot_app.api import apiauth
from .services import events_today
from django.core.handlers.wsgi import WSGIRequest

api = NinjaAPI(urls_namespace='eventsapi')


class ScheduleResponse(Schema):
    message: str = Field(...)


class ErrorResponse(Schema):
    reason: str = Field()


@api.get("/today", response={200: ScheduleResponse, 404: ErrorResponse}, auth=apiauth)
def today_schedule(request: WSGIRequest):
    events = events_today()
    message = ""
    if not events.exists():
        return 404, ErrorResponse(reason="There is no such events")
    for e in events:
        message += f"{str(e)}\n"

    return 200, ScheduleResponse(message=message)