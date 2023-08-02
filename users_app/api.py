from ninja import NinjaAPI, ModelSchema, Schema
from .models import User, Team
from django.core.exceptions import ObjectDoesNotExist

api = NinjaAPI(urls_namespace="userapi")


class BotRegisterSchema(Schema):
    username: str = "IvanII"


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'first_name', 'last_name', 'telegram', 'qr', 'team']


class TeamSchema(ModelSchema):
    class Config:
        model = Team
        model_fields = ['id', 'name', 'balance', 'tutor']


@api.post("/register", response=UserSchema)
def register(request, data: BotRegisterSchema):
    telegram = data.username
    user = User.objects.get(telegram=telegram)

    return user


@api.get("/team", response=TeamSchema)
def get_team(request, user_id: int):
    user = User.objects.get(pk=user_id)
    team = user.team
    return team
