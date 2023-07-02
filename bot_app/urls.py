from django.contrib import admin
from django.urls import path
from .views import test, qrscanner_page, api_checkinitdata, api_scanned

urlpatterns = [
    path('test/', test),
    path('qrscanner/', qrscanner_page),
    path('checkInitData', api_checkinitdata),
    path('scanned', api_scanned)
]