from django.urls import path

from .api import api as bot_api
from .views import qrscanner_page, error_page, specific_log

urlpatterns = [
    path('scanner', qrscanner_page),
    path('error/<int:error_id>/', error_page),
    path('api/', bot_api.urls),
    path('logs/<str:filename>/', specific_log)
]