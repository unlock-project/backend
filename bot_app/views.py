from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, Http404
from django.shortcuts import render
from .models import Error


def qrscanner_page(request):
    return render(request, "qrscanner/index.html")


def has_access_to_traceback(user) -> bool:
    #  add there permissions checking (function should return bool)
    return user.is_staff


@user_passes_test(has_access_to_traceback)
def error_page(request, error_id):
    if Error.objects.filter(id=error_id).exists():
        return render(request, f"tracebacks/error{error_id}.html")
    raise Http404()
