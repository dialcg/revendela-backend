from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model
from tickets.models import Ticket
from events.models import Event, Venue, EventCategory, Organizer

CustomUser = get_user_model()

class TicketSignalTests(TestCase):
    def setUp(self):
        self.buyer = CustomUser.objects.create_user(
            username="buyer", email="buyer@example.com", password="password", role=CustomUser.BUYER
        )
        self.seller = CustomUser.objects.create_user(
            username="seller", email="seller@example.com", password="password", role=CustomUser.SELLER
        )
        self.category = EventCategory.objects.create(name="Music")
        self.venue = Venue.objects.create(name="Stadium", address="123 Main St")
        self.organizer = Organizer.objects.create(name="Organizer Inc.")
        self.event = Event.objects.create(
            name="Concert",
            venue=self.venue,
            category=self.category,
            organizer=self.organizer,
        )
        self.ticket = Ticket.objects.create(
            event=self.event,
            resale_price=100.00,
            purchase_status=Ticket.AVAILABLE,
            seller=self.seller,
            venue_location="Section A, Row 1",
        )

    def test_notify_ticket_sent(self):
        self.ticket.purchase_status = Ticket.SENT
        self.ticket.buyer = self.buyer
        self.ticket.save()

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Tu ticket ha sido enviado", mail.outbox[0].subject)
        self.assertIn(self.buyer.email, mail.outbox[0].to)

    def test_notify_ticket_closed(self):
        self.ticket.purchase_status = Ticket.CLOSED
        self.ticket.save()

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Tu ticket ha sido cerrado", mail.outbox[0].subject)
        self.assertIn(self.seller.email, mail.outbox[0].to)