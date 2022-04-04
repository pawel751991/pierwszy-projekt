import uuid

import pytest

from sklint.models import *
from sklint.forms import *


@pytest.fixture
def test_password():
    p = "password"
    return p


@pytest.fixture
def create_user(django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def login_user(client, create_user, test_password):
    def make_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_login


@pytest.fixture
def client_registration():
    data = {
        "username": "username",
        "password": "password",
        "email": "email"
    }
    return data

@pytest.fixture
def category():
    c = Category.objects.create(
        title="Procesory"
    )
    return c


@pytest.fixture
def product():
    data = {
        "title": "Test product",
        "description": "Test product",
        "price": "10.02"
    }
    return data


@pytest.fixture
def product_created():
    pc = Product.objects.create(
        title="myszka",
        description="bezprzewodowa",
        price="10.02"
    )
    return pc


@pytest.fixture
def order():
    data = {
        "ordered_by": "test order",
        "address": "address",
        "mobile": "123456789",
        "email": "testorder@test.com"
    }
    return data


@pytest.fixture
def checkout():
    data = {
        "ordered_by": "Zamawiający",
        "address": "Adres dostawy",
        "mobile": "123456789"
    }
    return data
