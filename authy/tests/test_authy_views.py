import pytest
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from authy.models import CustomUser as User
from authy.views import MyAccountAdapter


@pytest.mark.django_db
def test_get_login_redirect_url_buyer(client):
    user = User.objects.create_user(username="buyer", password="password")
    user.role = "buyer"
    user.save()
    request = client.request().wsgi_request
    request.user = user
    adapter = MyAccountAdapter()

    redirect_url = adapter.get_login_redirect_url(request)

    assert redirect_url == reverse("buyer_tickets")


@pytest.mark.django_db
def test_get_login_redirect_url_seller(client):
    user = User.objects.create_user(username="seller", password="password")
    user.role = "seller"
    user.save()
    request = client.request().wsgi_request
    request.user = user
    adapter = MyAccountAdapter()

    redirect_url = adapter.get_login_redirect_url(request)

    assert redirect_url == reverse("seller_tickets")

