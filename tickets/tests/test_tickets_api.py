import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from events.models import Event, Venue, EventCategory, Organizer
from tickets.models import Ticket

@pytest.mark.django_db
def test_create_ticket():
    client = APIClient()
    User = get_user_model()
    seller = User.objects.create_user(username="selleruser", password="testpassword", role="SELLER")

    token_response = client.post("/authy/api/token/", {"username": seller.username, "password": "testpassword"})
    
    access_token = token_response.data["access"]

    category = EventCategory.objects.create(name="Electronic Music")
    venue = Venue.objects.create(name="Main Arena", address="123 Street")
    organizer = Organizer.objects.create(name="Event Organizer")
    event = Event.objects.create(name="Test Event", category=category, venue=venue, organizer=organizer)

    ticket_data = {
        "event": event.id,
        "resale_price": 50.00,
        "purchase_status": "AVAILABLE",
        "seller": seller.id,
        "venue_location": "Main Stage"
    }
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = client.post("/tickets/tickets/", ticket_data, format="json")

    assert response.status_code == 201
    assert Ticket.objects.count() == 1

@pytest.mark.django_db
def test_list_tickets_unauthorized():
    client = APIClient()
    response = client.get("/tickets/tickets/")

    assert response.status_code == 401 

@pytest.mark.django_db
def test_list_available_tickets():
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")

    token_response = client.post("/authy/api/token/", {"username": user.username, "password": "testpassword"})
    access_token = token_response.data["access"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/tickets/tickets/available/", headers=headers)

    assert response.status_code == 200 
    assert isinstance(response.data, list)  

@pytest.mark.django_db
def test_list_purchased_tickets():
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username="buyeruser", password="testpassword")

    token_response = client.post("/authy/api/token/", {"username": user.username, "password": "testpassword"})
    access_token = token_response.data["access"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/tickets/tickets/purchased/", headers=headers)

    assert response.status_code == 200  
    assert isinstance(response.data, list) 

@pytest.mark.django_db
def test_update_ticket_status_seller():
    client = APIClient()
    User = get_user_model()
    seller = User.objects.create_user(username="selleruser", password="testpassword", role="seller")

    token_response = client.post("/authy/api/token/", {"username": seller.username, "password": "testpassword"})
    
    access_token = token_response.data["access"]

    category = EventCategory.objects.create(name="Electronic Music")
    venue = Venue.objects.create(name="Main Arena", address="123 Street")
    organizer = Organizer.objects.create(name="Event Organizer")
    event = Event.objects.create(name="Test Event", category=category, venue=venue, organizer=organizer)
    
    ticket = Ticket.objects.create(event=event, resale_price=50.00, purchase_status="AVAILABLE", seller=seller, venue_location="Zone A")

    image = SimpleUploadedFile("ticket.jpg", b"file_content", content_type="image/jpeg")

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put(f"/tickets/tickets/{ticket.unique_identifier}/update-status-seller/", {"image": image}, format="multipart", headers=headers)

    assert response.status_code == 200
    ticket.refresh_from_db()
    assert ticket.purchase_status == Ticket.SENT

@pytest.mark.django_db
def test_update_ticket_status_buyer():
    client = APIClient()
    User = get_user_model()
    seller = User.objects.create_user(username="selleruser", password="testpassword", role="seller")
    buyer = User.objects.create_user(username="buyeruser", password="testpassword", role="buyer")

    token_response = client.post("/authy/api/token/", {"username": buyer.username, "password": "testpassword"})
    
    access_token = token_response.data["access"]

    category = EventCategory.objects.create(name="Electronic Music")
    venue = Venue.objects.create(name="Main Arena", address="123 Street")
    organizer = Organizer.objects.create(name="Event Organizer")
    event = Event.objects.create(name="Test Event", category=category, venue=venue, organizer=organizer)
    
    ticket = Ticket.objects.create(event=event, resale_price=50.00, purchase_status="SOLD", seller=seller, buyer=buyer, venue_location="Zone A")

    url = f"/tickets/tickets/{ticket.unique_identifier}/update-status-buyer/"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put(url, headers=headers)

    assert response.status_code == 200
    ticket.refresh_from_db()
    assert ticket.purchase_status == Ticket.CLOSED