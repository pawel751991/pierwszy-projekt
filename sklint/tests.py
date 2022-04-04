"""import pytest

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import reverse
from sklint.views import *


@pytest.mark.django_db
def test_home(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_registration(client, client_registration):
    url = reverse("clientregistration")
    data = {"email": "client@example.com", "password": "password"}
    form = ClientRegisterForm(data=client_registration)
    response = client.post(url, data)
    assert response.status_code == 200
    assert form.is_valid()


@pytest.mark.django_db
def test_login(login_user):
    client, user = login_user()
    url = reverse('clientlogin')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_is_valid():
    data = {"username": "username", "password": "password"}
    form = ClientLoginForm(data=data)
    assert form.is_valid()


@pytest.mark.django_db
def test_logout(client):
    url = reverse("clientlogout")
    response = client.get(url, follow=True)
    assert isinstance(response.context["user"], AnonymousUser)


@pytest.mark.django_db
def test_all_categories(client):
    categories_url = reverse('allcategories')
    response = client.get(categories_url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_category(client, category):
    response = client.get(category)
    assert str(category) == "Procesory"
    assert response.status_code == 404


@pytest.mark.django_db
def test_product(client, product, product_created):
    url = "productdetail"
    response = client.get(url)
    data = {
        "title": "Test product",
        "description": "Test product",
        "price": "10.02"
    }
    assert data == product
    assert response.status_code == 404
    assert len(Product.objects.all()) == 1
    assert Product.objects.get(title="myszka") == product_created
    assert Product.objects.get(description="bezprzewodowa") == product_created
    assert Product.objects.get(price="10.02") == product_created


@pytest.mark.django_db
def test_order_is_exist(client, order):
    url = reverse("orderhistory")
    response = client.get(url)
    data = {
        "ordered_by": "test order",
        "address": "address",
        "mobile": "123456789",
        "email": "testorder@test.com"
    }
    assert response.status_code == 302
    assert data == order


@pytest.mark.django_db
def test_checkout_is_exist(client):
    url = reverse("checkout")
    response = client.get(url)
    assert response.status_code == 302
    assert response.request["PATH_INFO"] == url


@pytest.mark.django_db
def test_checkout_form(checkout):
    form = CheckoutForm(data=checkout)
    assert form.is_valid()


@pytest.mark.django_db
def test_my_cart(client):
    url = reverse('mycart')
    response = client.get(url)
    assert response.status_code == 200"""
