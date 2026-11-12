from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .models import User


def home(request):
    if request.user.is_authenticated:
        return redirect("exams:list")
    return render(request, "users/home.html")


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "role")


def register(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("exams:list")
    return render(request, "users/register.html", {"form": form})
