from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")  # Redirect to a success page.
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def lougout_view(request):
    logout(request)
    return redirect("login")  # Redirect to a success page.


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect to a success page.
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def home(request):
    return render(request, "home.html")