from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import LoginForm, ProfileForm, UserForm


def user_register(request):

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.GET.get("next")
            print(next_url)
            if next_url:
                return redirect(next_url)
            return redirect("home")

    else:
        form = UserForm()
    return render(request, "signup.html", {"form": form})


def user_login(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect("home")

            else:
                form.add_error(None, "Invalid username or password.")
                return render(request, "login.html", {"form": form})
    else:
        form = LoginForm()
        return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")


@method_decorator(login_required(login_url="login"), name="dispatch")
class EditProfile(View):

    def get(self, request):
        user = request.user
        form = ProfileForm(instance=user)

        return render(request, "edit_profile.html", {"form": form, "user": user})

    def post(self, request):
        user = request.user
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect("home")

        return render(request, "edit_profile.html", {"form": form, "user": user})
