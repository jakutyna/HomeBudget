from django.urls import path

from .views import AddCategoryView, AddExpenseView, AddMonthBudgetView, AddMonthCategoryView, AddMonthView, \
    MonthView, MyBudgetView, UpdateMonthBudgetView

app_name = 'homebudget_app'
urlpatterns = [
    path('', MyBudgetView.as_view(), name='mybudget'),
    path('add-month/', AddMonthView.as_view(), name='add_month'),
    path('add-category/', AddCategoryView.as_view(), name='add_category'),
    path('month/<int:pk>-<slug:slug>/', MonthView.as_view(), name='month'),
    path('month/<int:pk>-<slug:slug>/add-month-budget/', AddMonthBudgetView.as_view(), name='add_month_budget'),
    path('month/<int:pk>-<slug:slug>/update-month-budget/', UpdateMonthBudgetView.as_view(), name='update_month_budget'),
    path('month/<int:pk>-<slug:slug>/add-month-category/', AddMonthCategoryView.as_view(), name='add_month_category'),
    path('month/<int:pk>-<slug:slug>/add-expense/<int:mc_pk>/', AddExpenseView.as_view(), name='add_expense'),
]