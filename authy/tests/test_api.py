import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_create_token():
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")

    response = client.post(
        "/authy/api/token/", {"username": user.username, "password": "testpassword"}
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_refresh_token():
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")

    response = client.post(
        "/authy/api/token/", {"username": user.username, "password": "testpassword"}
    )
    refresh_token = response.data["refresh"]

    response = client.post("/authy/api/token/refresh/", {"refresh": refresh_token})

    assert response.status_code == 200
    assert "access" in response.data
