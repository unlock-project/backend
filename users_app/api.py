from ninja import NinjaAPI, ModelSchema, Schema
from .models import User

api = NinjaAPI()


class BotRegisterSchema(Schema):
    username: str = "IvanII"


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'first_name', 'last_name', 'telegram']


@api.post("/register", response=UserSchema)
def register(request, data: BotRegisterSchema):
    telegram = data.username
    user = User.objects.get(telegram=telegram)

    return user
