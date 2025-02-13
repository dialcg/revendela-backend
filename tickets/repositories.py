from .models import Ticket
from events.models import Event
from decimal import Decimal
from authy.models import CustomUser


class TicketRepository:
    @staticmethod
    def create_ticket(
        event: Event,
        resale_price: Decimal,
        venue_location: str,
        purchase_status: str,
        seller: CustomUser,
    ) -> Ticket:
        ticket: Ticket = Ticket.objects.create(
            event=event,
            resale_price=resale_price,
            venue_location=venue_location,
            purchase_status=purchase_status,
            seller=seller,
        )
        return ticket

    @staticmethod
    def get_tickets_by_uuid(uuid: str) -> Ticket:
        return Ticket.objects.get(unique_identifier=uuid)

    @staticmethod
    def get_buyer_tickets(user: CustomUser):
        return Ticket.objects.filter(buyer=user)

    @staticmethod
    def get_seller_tickets(user: CustomUser):
        return Ticket.objects.filter(seller=user)

    @staticmethod
    def get_all_tickets_status_available():
        return Ticket.objects.filter(purchase_status=Ticket.AVAILABLE)

    @staticmethod
    def get_all_tickets_not_user(user: CustomUser):
        return Ticket.objects.exclude(seller=user).filter(
            purchase_status=Ticket.AVAILABLE
        )
        
    @staticmethod
    def update_ticket_status_seller(ticket_id):
        ticket = TicketRepository.get_tickets_by_uuid(ticket_id)
        ticket.purchase_status = Ticket.SENT
        ticket.save()
        return ticket

    @staticmethod
    def update_ticket_status_buyer(ticket_id):
        ticket = TicketRepository.get_tickets_by_uuid(ticket_id)
        ticket.purchase_status = Ticket.CLOSED
        ticket.save()
        return ticket
    
    @staticmethod
    def get_all_tickets():
        return Ticket.objects.all()

    @staticmethod
    def get_available_tickets():
        return Ticket.objects.filter(purchase_status="AVAILABLE")

    @staticmethod
    def get_user_tickets(user: CustomUser):
        return Ticket.objects.filter(buyer=user)
