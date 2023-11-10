# Django
from django.http import HttpResponse
from django.shortcuts import redirect


def return_200_view(request):
    return HttpResponse(status=200)


def redirect_admin_view(request):
    return redirect("/admin/")


def redirect_swagger_view(request):
    return redirect("/docs/")


def redirect_api_v1_view(request):
    return redirect("/api/v1/")


def redirect_api_v2_view(request):
    return redirect("/api/v2/")
