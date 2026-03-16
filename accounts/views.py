from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, LoginForm
from .models import User


def home(request):
    return render(request, 'base.html')

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
    def get(self, request):
        if request.method == 'GET':
            user = User.objects.get(id=request.session['user_id'])
            print(user)
            return render(request, 'edit_profile.html', {
                'user': user
            })
        else:
            form = UserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('home')
            return render(request, 'edit_profile.html', {'form': form})
