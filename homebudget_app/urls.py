from django.urls import path

from .views import AddMonthView, MonthView, MyBudgetView

app_name = 'homebudget_app'
urlpatterns = [
    path('', MyBudgetView.as_view(), name='mybudget'),
    path('add-month/', AddMonthView.as_view(), name='add_month'),
    path('<slug:month_slug>/', MonthView.as_view(), name='month'),
]