from decouple import config
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, View

from authy.models import CustomUser
from .repositories import TicketRepository
from events.repositories import EventRepository
from .models import Ticket
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"


class TicketSaleView(LoginRequiredMixin, TemplateView):
    template_name = "tickets/ticket.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != CustomUser.SELLER:
            messages.error(request, "No tienes permisos para acceder a esta página.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = EventRepository.get_all_events()
        context["ticket_status_choices"] = Ticket.STATUS_CHOICES

        return context

    def post(self, request):

        event_id = request.POST.get("event")
        resale_price = request.POST.get("resale_price")
        venue_location = request.POST.get("venue_location")
        purchase_status = request.POST.get("purchase_status")
        seller = request.user
        event = EventRepository.get_event_by_id(id=event_id)

        TicketRepository.create_ticket(
            event=event,
            resale_price=resale_price,
            venue_location=venue_location,
            purchase_status=purchase_status,
            seller=seller,
        )

        messages.add_message(
            request, messages.SUCCESS, "Se ha creado exitosamente el ticket"
        )

        return self.get(request)


class BuyerTicketListView(ListView):
    model = Ticket
    template_name = "tickets/buyer_tickets.html"
    context_object_name = "tickets"

    def get_queryset(self):
        return TicketRepository.get_buyer_tickets(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_tickets"] = TicketRepository.get_all_tickets_not_user(
            self.request.user
        )
        return context


class SellerTicketListView(ListView):
    model = Ticket
    template_name = "tickets/seller_tickets.html"
    context_object_name = "tickets"

    def get_queryset(self):
        return TicketRepository.get_seller_tickets(self.request.user)


class TicketDetailView(DetailView):
    model = Ticket
    template_name = "tickets/ticket_detail.html"
    context_object_name = "ticket"
    pk_url_kwarg = "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wompi_public_key"] = config("WOMPI_PUBLIC_KEY")
        return context


class TicketPurchaseView(View):
    def post(self, request, *args, **kwargs):
        ticket_id = kwargs.get("uuid")
        try:
            ticket = TicketRepository.get_tickets_by_uuid(ticket_id)

            if ticket.purchase_status == Ticket.AVAILABLE:
                ticket.buyer = request.user
                ticket.purchase_status = Ticket.SOLD
                ticket.save()
                messages.success(request, "¡Has comprado el ticket con éxito!")
            else:
                messages.error(request, "El ticket ya no está disponible.")

        except Ticket.DoesNotExist:
            messages.error(request, "El ticket no existe.")

        return HttpResponseRedirect(
            reverse("ticket_detail", kwargs={"uuid": ticket_id})
        )
