import datetime, pytest

from django.contrib.auth.models import User

from homebudget_app.models import Category, Expense, Month, MonthBudget, MonthCategory


@pytest.fixture
def mybudget_data():
    user = User.objects.create_user(username='PytestUser', password='Pytest151900')
    user2 = User.objects.create_user(username='PytestUser2', password='Pytest151900')

    january_2021 = Month.objects.create(month_name=Month.JANUARY, year=2020,
                                        month_beginning_date=datetime.date(2020, 1, 1),
                                        month_end_date=datetime.date(2020, 1, 31),
                                        slug='january-2020', user=user)
    february_2021 = Month.objects.create(month_name=Month.FEBRUARY, year=2020,
                                         month_beginning_date=datetime.date(2020, 2, 1),
                                         month_end_date=datetime.date(2020, 2, 28),
                                         slug='february-2020', user=user)

    january_2021_2 = Month.objects.create(month_name=Month.JANUARY, year=2020,
                                          month_beginning_date=datetime.date(2020, 1, 1),
                                          month_end_date=datetime.date(2020, 1, 31),
                                          slug='january-2020', user=user2)

    shopping = Category.objects.create(name='shopping', description='', slug='shopping', user=user)
    other = Category.objects.create(name='other', description='some stuff', slug='other', user=user)

    january_2021_budget = MonthBudget.objects.create(budget=4850.85, month=january_2021)

    january_2021_shopping = MonthCategory.objects.create(category_budget='1000', month=january_2021,
                                                         category=shopping)
    january_2021_other = MonthCategory.objects.create(category_budget='2200', month=january_2021,
                                                      category=other)

    expense_groceries = Expense.objects.create(name='groceries', expense_amount=120,
                                               month_category=january_2021_shopping)
    expense_clothes = Expense.objects.create(name='clothes', expense_amount=400,
                                               month_category=january_2021_shopping)

    data = {
        'user': user,
        'user2': user2,
        'months': [february_2021, january_2021],
        'months2': [january_2021_2],
        'categories': [other, shopping],
        'month_budget': january_2021_budget,
        'month_categories': [january_2021_shopping, january_2021_other],
        'expenses': [expense_groceries, expense_clothes]
    }
    return data
