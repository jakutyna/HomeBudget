from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views import View

from .forms import CustomAuthenticationForm


class HomeView(View):
    """View with project homepage"""
    def get(self, request, *args, **kwargs):
        return render(request, 'main/home.html')


class LoginUserView(LoginView):
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True
    template_name = 'main/login.html'


class LogoutUserView(LogoutView):
    pass


class RegisterUserView(View):
    pass


class UserView(View):
    """View with user profile. Enables user to manage account settings."""
    pass
