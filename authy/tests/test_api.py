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
def test_create_token_invalid_credentials():
    client = APIClient()
    User = get_user_model()
    User.objects.create_user(username="testuser", password="testpassword")

    response = client.post(
        "/authy/api/token/", {"username": "testuser", "password": "wrongpassword"}
    )

    assert response.status_code == 401  
    assert "access" not in response.data
    assert "refresh" not in response.data

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

@pytest.mark.django_db
def test_logout_success():
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")

    response = client.post(
        "/authy/api/token/", {"username": user.username, "password": "testpassword"}
    )
    
    access_token = response.data["access"]  
    refresh_token = response.data["refresh"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = client.post("/authy/api/token/logout/", {"refresh": refresh_token})

    assert response.status_code == 205 
    assert response.data["message"] == "Logout successful"
    
@pytest.mark.django_db
def test_logout_invalid_token():
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="password")
    client = APIClient()

    response = client.post("/authy/api/token/", {"username": "testuser", "password": "password"})
    access_token = response.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = client.post("/authy/api/token/logout/", {"refresh": "invalid_token"})

    assert response.status_code == 400
    assert response.data["error"] == "Invalid token"

@pytest.mark.django_db
def test_logout_no_token():
    
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="password")
    client = APIClient()

    response = client.post("/authy/api/token/", {"username": "testuser", "password": "password"})
    access_token = response.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = client.post("/authy/api/token/logout/", {})

    assert response.status_code == 400 
    assert response.data["error"] == "Invalid token"

