import pytest

from django.contrib import auth
from homebudget_app.models import MonthBudget


def test_mybudget_view_client_not_logged(client):
    url = '/mybudget/'
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain == [('/login/?next=/mybudget/', 302)]


@pytest.mark.django_db
def test_mybudget_view_client_logged(client, mybudget_data):
    client.force_login(user=mybudget_data['user'])
    assert auth.get_user(client).is_authenticated == True
    url = '/mybudget/'
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain == []
    assert len(response.context['months']) == 2
    assert len(response.context['categories']) == 2
    assert response.context['months'][0] == mybudget_data['months'][0]
    assert response.context['months'][1] == mybudget_data['months'][1]
    assert response.context['categories'][0] == mybudget_data['categories'][0]
    assert response.context['categories'][1] == mybudget_data['categories'][1]


@pytest.mark.django_db
def test_month_view_not_users_month(client, mybudget_data):
    client.force_login(user=mybudget_data['user'])
    assert auth.get_user(client).is_authenticated == True
    not_users_month = mybudget_data['months2'][0]
    pk_slug = '{}-{}'.format(not_users_month.pk, not_users_month.slug)
    url = '/mybudget/month/{}/'.format(pk_slug)
    response = client.get(url, follow=True)
    assert response.status_code == 404


@pytest.mark.django_db
def test_month_view_users_month(client, mybudget_data):
    client.force_login(user=mybudget_data['user'])
    assert auth.get_user(client).is_authenticated == True
    category_expenses = mybudget_data['expenses'][0].expense_amount + mybudget_data['expenses'][1].expense_amount
    users_month = mybudget_data['months'][1]
    pk_slug = '{}-{}'.format(users_month.pk, users_month.slug)
    url = '/mybudget/month/{}/'.format(pk_slug)
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert response.context['month_budget'] == mybudget_data['month_budget']
    assert len(response.context['month_categories']) == 2
    assert response.context['month_categories'][0] == mybudget_data['month_categories'][0]
    assert response.context['month_categories'][1] == mybudget_data['month_categories'][1]
    assert response.context['month_categories'][0].category_expenses == category_expenses
    assert response.context['total_sum_and_diff'][0] == category_expenses
    assert float(response.context['total_sum_and_diff'][1]) == mybudget_data['month_budget'].budget - category_expenses


@pytest.mark.django_db
def test_update_month_budget(client, mybudget_data):
    client.force_login(user=mybudget_data['user'])
    assert auth.get_user(client).is_authenticated == True
    users_month = mybudget_data['months'][1]
    pk_slug = '{}-{}'.format(users_month.pk, users_month.slug)
    url = '/mybudget/month/{}/update-month-budget/'.format(pk_slug)

    response_get = client.get(url, follow=True)
    assert response_get.status_code == 200
    assert mybudget_data['month_budget'].budget == 4850.85

    response_post = client.post(url, {'budget': '4500'}, follow=True)
    assert response_post.status_code==200
    redirect_url = '/mybudget/month/{}/'.format(pk_slug)
    assert response_post.redirect_chain == [(redirect_url, 302)]
    updated_budget = MonthBudget.objects.get(pk=mybudget_data['month_budget'].pk)
    assert updated_budget.budget == 4500