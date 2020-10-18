from django.contrib import admin
from django.urls import include, path

from main.views import HomeView, LoginUserView, LogoutUserView, RegisterUserView, UserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('user/', UserView.as_view(), name='user'),
    path('mybudget/', include('homebudget_app.urls')),
]
