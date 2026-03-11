from django.views import View
from django.shortcuts import render, redirect


class SignUp(View):
    def get(self, request):
        return render(request, 'signup.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')


class LogOut(View):
    def get(self, request):
        return redirect(request, 'sign-up/')


class EditProfile(View):
    def get(self, request):
        return render(request, 'edit_profile.html')
