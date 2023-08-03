from .models import *
import datetime


def events_today():
    today = datetime.date.today()
    events = Attendance.objects.filter(date=today)

    return events
