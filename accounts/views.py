from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import UserForm, LoginForm, ProfileForm


def user_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
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


@method_decorator(login_required(login_url='login'), name='dispatch')
class EditProfile(View):

    def get(self, request):
        user = request.user
        form = ProfileForm(instance=user)
        return render(request, 'edit_profile.html', {
            'form': form,
            'user': user
        })

    def post(self, request):
        user = request.user
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('home')

        return render(request, 'edit_profile.html', {
            'form': form,
            'user': user
        })
