from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/home.html')


class LoginUserView(View):
    def get(self, request, *args, **kwargs):
        pass


class LogoutUserView(View):
    def get(self, request, *args, **kwargs):
        pass


class RegisterUserView(View):
    def get(self, request, *args, **kwargs):
        pass
