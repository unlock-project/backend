from ninja import NinjaAPI, ModelSchema, Schema
from pydantic import Field
from unlock.settings import BASE_DIR
from .models import User, Team
from django.core.exceptions import ObjectDoesNotExist
import secrets


api = NinjaAPI(urls_namespace="userapi")


class BotRegisterSchema(Schema):
    username: str = "IvanII"


class ErrorNotFound(Schema):
    error: str = "Not found"


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'first_name', 'last_name', 'telegram', 'qr', 'team']


class TeamSchema(ModelSchema):
    class Config:
        model = Team
        model_fields = ['id', 'name', 'balance', 'tutor']


class BalanceSchema(Schema):
    user_id: int = Field(...)
    balance: int = Field(...)


@api.post("/register", response=UserSchema)
def register(request, data: BotRegisterSchema):
    telegram = data.username
    user = User.objects.get(telegram=telegram)
    return user


@api.get("/team", response={200: TeamSchema, 400: ErrorNotFound})
def get_team(request, user_id: int):
    user = User.objects.get(pk=user_id)
    team = user.team
    if team is not None:
        return team

    return 400, ErrorNotFound(error="У пользователя нет команды")


@api.get("/balance", response=BalanceSchema)
def get_balance(request, user_id: int):
    user = User.objects.get(pk=user_id)
    return BalanceSchema(user_id=user.id, balance=user.balance)


# @api.get("/gen/org", response=UserSchema)
# def get_balance(request):
#     passwords = []
#     with open(BASE_DIR / "data organizers.csv", "r") as file:
#         for row in file:
#             arr = row.strip().split(",")
#             username = arr[2]
#             first_name = arr[1]
#             last_name = arr[0]
#             telegram = arr[2]
#             password = secrets.token_hex(5)
#             passwords.append(username + ", "+ password + "\n")
#             user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, telegram=telegram, password=password)
#             user.save()
#
#     with open(BASE_DIR / "credits.csv", "w") as file:
#         file.writelines(passwords)
#
#     return user
