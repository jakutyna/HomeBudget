from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request, *args, **kwargs):
        pass

class LoginView(View):
    def get(self, request, *args, **kwargs):
        pass

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        pass

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        pass