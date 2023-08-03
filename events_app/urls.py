from django.contrib.auth.decorators import login_required
from django.urls import path
from .api import api as eventsapi

urlpatterns = [
    path('', eventsapi.urls),

]