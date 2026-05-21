from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, "core/home.html", {"service_name": "Django Local Server"})


def health(request):
    return JsonResponse({"status": "ok", "service": "django-local-server"})
