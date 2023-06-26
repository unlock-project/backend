from django.contrib import admin
from django.urls import path
from .api import api as user_api

urlpatterns = [
    path('', user_api.urls),
]
