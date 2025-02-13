from decouple import config
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, View

from authy.models import CustomUser
from .repositories import TicketRepository
from events.repositories import EventRepository
from .models import Ticket
from django.views.generic import TemplateView

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import TicketSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


class TicketViewSet(viewsets.ModelViewSet):
    queryset = TicketRepository.get_all_tickets()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        available_tickets = TicketRepository.get_available_tickets()
        serializer = TicketSerializer(available_tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def purchased(self, request):
        user_tickets = TicketRepository.get_user_tickets(request.user)
        serializer = TicketSerializer(user_tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['put'], url_path='update-status-seller')
    def update_status_seller(self, request, pk=None):
        if request.user.role != CustomUser.SELLER:
            return Response({"error": "No tienes permisos para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)
        
        if 'image' not in request.FILES:
            return Response({"error": "Se requiere una imagen para actualizar el estado."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            TicketRepository.update_ticket_status_seller(pk)
            return Response({"message": "Ticket marcado como ENVIADO"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update-status-buyer')
    def update_status_buyer(self, request, pk=None):
        if request.user.role != CustomUser.BUYER:
            return Response({"error": "No tienes permisos para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            TicketRepository.update_ticket_status_buyer(pk)
            return Response({"message": "Ticket marcado como CERRADO"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

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
