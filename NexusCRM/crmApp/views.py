from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

# Create your views here.

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if not user.is_active:
                messages.error(
                    request,
                    "Your account has been disabled. Please contact an administrator."
                )

                return render(
                    request,
                    "auth/login.html"
                )

            login(request, user)

            next_url = request.POST.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "auth/login.html"
    )

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def module_placeholder(request, module_name):
    return render(request, "placeholder.html",
        {
            "module_name": module_name,
        }
    )

@login_required
def logout_view(request):

    if request.method == "POST":

        logout(request)

        return redirect("login")

    return redirect("dashboard")

