from .models import *
import datetime


def events_today():
    today = datetime.date.today()
    events = Event.objects.filter(date=today, polymorphic_ctype_id__in=(17, 18))

    return events
