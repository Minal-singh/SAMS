"""
Common views shared for admin and students both.
"""

from django.shortcuts import redirect, render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .email_backend import EmailBackend


def handle_not_found(request, exception):
    return render(request, '_partials/error_404.html')


def handle_server_error(request):
    return render(request, '_partials/error_404.html')


def index(request):
    return HttpResponseRedirect(reverse("login"))


def login_user(request, **kwargs):
    if request.user.is_authenticated:
        if request.user.user_type == "1":
            return redirect(reverse("admin_home"))
        else:
            return redirect(reverse("student_home"))

    if request.method == "GET":
        return render(request, "main/login.html")

    if request.method == "POST":
        context = {"data": request.POST, "has_error": False}
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email == "":
            messages.add_message(request, messages.ERROR, "Email is required")
            context["has_error"] = True
        if password == "":
            messages.add_message(request, messages.ERROR, "Password is required")
            context["has_error"] = True

        user = EmailBackend.authenticate(request, username=email, password=password)

        if not user and not context["has_error"]:
            messages.add_message(request, messages.ERROR, "Invalid login credentials")
            context["has_error"] = True

        if context["has_error"]:
            return render(request, "main/login.html", status=401, context=context)

        if user is not None:
            login(request, user)
            if user.user_type == "1":
                return redirect(reverse("admin_home"))
            else:
                return redirect(reverse("student_home"))


def logout_user(request):
    if request.user is not None:
        logout(request)
    return redirect(reverse("login"))
