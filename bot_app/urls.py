from django.contrib import admin
from django.urls import path
from .views import test, qrscanner_page
from .api import api as bot_api

urlpatterns = [
    path('scanner', qrscanner_page),
    # path('test/', test),
    # path('checkInitData', api_checkinitdata),
    # path('scanned', api_scanned)
    path('api/', bot_api.urls)
]