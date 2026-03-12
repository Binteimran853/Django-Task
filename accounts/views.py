from django.views import View
from django.shortcuts import render, redirect
from .models import User


class Home(View):
    def get(selfself, request):
        return render(request, 'base.html')


class SignUp(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = User(
            user_name=username,
            email=email,
            password=password
        )
        user.save()

        return redirect('sign-up')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = User.objects.filter(user_name=username, password=password)
        if user:
            return redirect('edit-profile')
        return redirect('login')


class LogOut(View):
    def get(self, request):
        return redirect(request, 'sign-up/')


class EditProfile(View):
    def get(self, request):
        return render(request, 'edit_profile.html')
