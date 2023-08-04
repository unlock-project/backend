from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import secrets


# Create your models here.
def generateQrData():
    return secrets.token_hex(3)

class Team(models.Model):
    name = models.CharField(max_length=100)
    balance = models.IntegerField(default=0)
    tutor = models.OneToOneField("User", related_name="tutor", null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class User(AbstractUser):
    object = CustomUserManager()

    REQUIRED_FIELDS = ['first_name', 'last_name', ]
    team = models.ForeignKey(to=Team, null=True, blank=True, on_delete=models.DO_NOTHING)
    balance = models.IntegerField(default=0)
    telegram = models.CharField(max_length=100, null=True, blank=True)
    qr = models.CharField(max_length=100, unique=True, blank=True, default=generateQrData)
    is_organizer = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def all_users():
        return User.objects.all()


