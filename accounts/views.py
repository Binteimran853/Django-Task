from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, LoginForm
from .models import User


def home(request):
    user = User.objects.get(id=request.user.id)
    return render(request, 'base.html', {'user': user})


def user_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'signup.html', {'form': form})

    else:
        form = UserForm()
        return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form = LoginForm()
                error_message = 'user not registered, sign up first'
                return render(request, 'login.html', {
                            'error_message': error_message,
                            'form': form
                        })
        return render(request, 'signup.html', {'form': form})

    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


class EditProfile(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            print(user.username)
            return render(request, 'edit_profile.html', {
                'user': user
            })
        else:
            print('user not logged in')
            return redirect('login')

    @staticmethod
    def post(request):
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            username = request.POST.get('username')
            email = request.POST.get('email')
            user.username = username
            user.email = email
            user.save()
            return redirect('home')
        else:
            error_message = 'user not logged in'
            return render(request, 'edit_profile.html', {
                'error_message': error_message
            })
