from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from front.views import main_page, qr_generator_page, user_ids_page, send_msg_page, logs_page, users_page

urlpatterns = [
    path('', login_required(main_page), name='index'),
    path('qrgenerator', login_required(qr_generator_page), name='qrgenerator'),
    path('userids', login_required(user_ids_page), name='userids'),
    path('sendmsg', login_required(send_msg_page), name='sendmsg'),
    path('logs', login_required(logs_page), name='logs'),
    path('users', login_required(users_page), name='users'),
]