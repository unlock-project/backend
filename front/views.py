from django.shortcuts import render, redirect


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