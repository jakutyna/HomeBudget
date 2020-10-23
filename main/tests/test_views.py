import pytest

from django.contrib import auth


@pytest.mark.django_db
def test_login(client, user_pytest):
    assert client.login(username='PytestUser', password='Pytest151900') == True


def test_home_view_get(client):
    url = ''
    response = client.get(url)
    assert response.status_code == 200


def test_login_view_get_client_not_logged(client):
    url = '/login/'
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_get_client_logged(client, user_pytest):
    client.force_login(user=user_pytest)
    assert auth.get_user(client).is_authenticated == True
    url = '/login/'
    response = client.get(url, follow = True)
    assert response.status_code == 200
    assert response.redirect_chain == [('/', 302)]


@pytest.mark.django_db
def test_login_view_post_valid(client, user_pytest):
    url = '/login/'
    response = client.post(url, {'username': 'PytestUser', 'password': 'Pytest151900'}, follow=True)
    assert response.status_code == 200
    assert response.context['user'] == user_pytest
    assert auth.get_user(client).is_authenticated == True
    assert client.session['_auth_user_id'] == str(user_pytest.pk)
    assert response.redirect_chain == [('/', 302)]


@pytest.mark.django_db
def test_login_view_post_invalid(client, user_pytest):
    url = '/login/'
    response = client.post(url, {'username': 'PytestUser', 'password': 'Pytest'}, follow=True)
    assert response.status_code == 200
    assert response.context['user'].is_anonymous == True
    assert auth.get_user(client).is_authenticated == False
    assert response.redirect_chain == []


@pytest.mark.django_db
def test_logout_view_client_not_logged(client):
    url = '/logout/'
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert auth.get_user(client).is_authenticated == False
    assert response.redirect_chain == [('/', 302)]


@pytest.mark.django_db
def test_logout_view_client_logged(client, user_pytest):
    client.force_login(user=user_pytest)
    assert auth.get_user(client).is_authenticated == True
    url = '/logout/'
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert auth.get_user(client).is_authenticated == False
    assert response.redirect_chain == [('/', 302)]
