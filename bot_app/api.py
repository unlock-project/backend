import requests
from ninja import NinjaAPI, Schema, Field
from django.conf import settings
from .services import checkinitdata

api = NinjaAPI()


class CheckInitDataRequest(Schema):
    auth: str = Field(...)


class CheckInitDataResponse(Schema):
    valid: bool = Field(...)
    chat_id: int = Field(...)


class ScannedRequest(Schema):
    auth: str = Field(...)
    qr_data: str = Field(...)


class Error(Schema):
    reason: str = Field()


# test
class ScannedResponse(Schema):
    user_id: int = Field(...)
    qr_data: str = Field(...)


@api.post("/checkinitdata", response=CheckInitDataResponse)
def checkinitdata_request(request, data: CheckInitDataRequest):
    response = checkinitdata(data.auth)
    return CheckInitDataResponse(**response)


@api.post("/scanned", response={200: ScannedResponse, 400: Error})
def scanned_request(request, data: ScannedRequest):
    checked_data = checkinitdata(data.auth)
    if 'valid' not in checked_data.keys() or not checked_data['valid'] or 'chat_id' not in checked_data.keys():
        return Error(reason="Not valid telegram web app data")
    chat_id = checked_data["chat_id"]  # User who scanned qr code
    try:
        user_id = requests.get(settings.BOT_URL + '/user/id', params={'chat_id': chat_id}).json()["user_id"]  # User who
    except Exception as ex:
        return Error(reason=ex.args)
    # scanned qr code
    qr_data = data.qr_data
    # CHECK IF USER IS ORGANIZER
    # DO MAGIC
    return ScannedResponse(user_id=user_id, qr_data=qr_data)
