from django.urls import path
from .api import api as bot_api
from .views import qrscanner_page, error_page

urlpatterns = [
    path('scanner', qrscanner_page),
    path('error/<int:error_id>/', error_page),
    path('api/', bot_api.urls),
]