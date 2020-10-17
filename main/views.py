from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views import View

from .forms import CustomAuthenticationForm


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/home.html')


class LoginUserView(LoginView):
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True
    template_name = 'main/login.html'


class LogoutUserView(LogoutView):
    pass


class RegisterUserView(View):
    def get(self, request, *args, **kwargs):
        pass
