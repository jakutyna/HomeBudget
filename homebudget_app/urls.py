from django.urls import path

from .views import AddCategoryView, AddMonthView, MonthView, MyBudgetView

app_name = 'homebudget_app'
urlpatterns = [
    path('', MyBudgetView.as_view(), name='mybudget'),
    path('add-month/', AddMonthView.as_view(), name='add_month'),
    path('add-category/', AddCategoryView.as_view(), name='add_category'),
    path('month/<int:pk>-<slug:slug>/', MonthView.as_view(), name='month'),
]