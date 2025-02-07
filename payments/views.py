import hashlib
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render
from decouple import config
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from .repositories import TransactionRepository
from tickets.repositories import TicketRepository
from tickets.models import Ticket
from uuid import UUID
from django.core.mail import send_mail
from rest_framework import status
from decouple import config


class PaymentPanelView(LoginRequiredMixin, TemplateView):
    template_name = "payments/payment.html"
    login_url = "/accounts/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wompi_public_key"] = config("WOMPI_PUBLIC_KEY")

        return context


class WompiWebhookApiView(APIView):
    def post(self, request, format=None):
        event_data = request.data
        secret = config("WOMPI_SECRET_KEY")

        transaction_data = event_data.get("data", {}).get("transaction", {})
        signature_data = event_data.get("signature", {})
        event_timestamp = event_data.get("timestamp")

        concatenated_values = ""
        for prop in signature_data.get("properties", []):
            if prop == "transaction.id":
                concatenated_values += str(transaction_data.get("id", ""))
            elif prop == "transaction.status":
                concatenated_values += str(transaction_data.get("status", ""))
            elif prop == "transaction.amount_in_cents":
                concatenated_values += str(transaction_data.get("amount_in_cents", ""))

        concatenated_values += str(event_timestamp)

        concatenated_values += secret

        calculated_checksum = hashlib.sha256(concatenated_values.encode()).hexdigest()

        provided_checksum = signature_data.get("checksum", "")
        if calculated_checksum != provided_checksum:
            return Response(
                {"message": "Webhook received but verification failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        wompi_id = transaction_data.get("id")
        print(wompi_id)
        transaction = TransactionRepository.get_transaction_by_wompi_id(wompi_id)

        if transaction:
            new_status = transaction_data.get("status")
            TransactionRepository.update_transaction_status(wompi_id, new_status)
            return Response(
                {"message": "Transaction status updated successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Transaction does not exist, no action taken"},
                status=status.HTTP_404_NOT_FOUND,
            )


class WompiRedirectTemplateView(TemplateView):
    template_name = "payments/redirect.html"

    def get(self, request, *args, **kwargs):
        id = request.GET.get("id", "")
        context = {"wompi_id": id}
        return render(request, self.template_name, context)


class WompiTransactionApiView(APIView):
    def post(self, request, format=None):
        wompi_id = request.data.get("wompi_id")
        amount_in_cents = request.data.get("amount")
        amount = int(amount_in_cents) / 100
        reference = request.data.get("reference")

        transaction = TransactionRepository.get_transaction_by_wompi_id(wompi_id)
        if transaction:
            return Response({"message": "Transaction already exists"}, status=400)

        TransactionRepository.create_transaction(
            wompi_id=wompi_id,
            reference=reference,
            amount=amount,
            status=request.data.get("status"),
            user=request.user,
        )
        try:
            ticket_id_str = reference.split("_")[0]
            ticket_id = UUID(ticket_id_str)
            ticket = TicketRepository.get_tickets_by_uuid(ticket_id)

            if ticket.purchase_status == Ticket.AVAILABLE:
                ticket.buyer = request.user
                ticket.purchase_status = Ticket.SOLD
                ticket.save()
                self.send_purchase_email(ticket)
                return Response({"message": "¡Ticket comprado con éxito!"})
            else:
                return Response(
                    {"error": "El ticket ya no está disponible."}, status=400
                )

        except (Ticket.DoesNotExist, ValueError):
            return Response(
                {"error": "El ticket no existe o el ID de referencia es inválido."},
                status=400,
            )

    @staticmethod
    def send_purchase_email(ticket):
        subject = "Confirmación de compra de ticket"
        message = f"""
        Hola {ticket.buyer.username},

        ¡Gracias por tu compra! Aquí tienes los detalles de tu ticket:

        - **Evento**: {ticket.event.name}
        - **Fecha y hora**: {ticket.event.date}
        - **Lugar**: {ticket.venue_location}
        - **Precio**: ${ticket.resale_price}
        - **Identificador del ticket**: {ticket.unique_identifier}

        Te esperamos en el evento.

        Saludos,
        El equipo de Tu Sitio.
        """
        recipient_list = [ticket.buyer.email]
        send_mail(subject, message, "noreply@tusitio.com", recipient_list)
