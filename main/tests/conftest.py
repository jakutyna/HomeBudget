from django.contrib.auth.models import User

import pytest


@pytest.fixture
def user_pytest():
    return User.objects.create_user(username='PytestUser', password='Pytest151900')
