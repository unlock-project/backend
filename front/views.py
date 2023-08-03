from django.shortcuts import render, redirect

from events_app.models import Attendance
from events_app.services import events_today
from users_app.models import User, Team


# Create your views here.
def main_page(request):
    if request.user.is_anonymous:
        return redirect(f'/accounts/login')
    return render(request, f"main/index.html")


def qr_generator_page(request):
    if request.user.is_anonymous:
        return redirect(f'/accounts/login')
    return render(request, f'main/qrgenerator.html')


def user_ids_page(request):
    if request.user.is_anonymous:
        return redirect(f'/accounts/login')
    return render(request, f'main/userids.html')


def send_msg_page(request):
    if request.user.is_anonymous:
        return redirect(f'/accounts/login')
    return render(request, f'main/sendmsg.html')


def logs_page(request):
    if request.user.is_anonymous:
        return redirect(f'/accounts/login')
    return render(request, f'main/logs.html')


def users_page(request):
    if request.user.is_anonymous:
        return redirect(f'/accounts/login')
    return render(request, f'main/users.html', {'users' : User.objects.all()})


def event_choose_page(request):
    if request.user.is_anonymous:
        return redirect(f'/accounts/login')
    event_today = events_today()
    print(event_today)
    return render(request, f'main/events.html', {'events': events_today})


def teams_page(request):
    if request.user.is_anonymous:
        return redirect(f'/accounts/login')
    return render(request, f'main/teams.html', {'teams' : Team.objects.all()})