from django.urls import path
from .views import (
    PaymentPanelView,
    WompiWebhookApiView,
    WompiRedirectTemplateView,
    WompiTransactionApiView,
)

urlpatterns = [
    path("", PaymentPanelView.as_view(), name="checkout"),
    path("wompi/webhook/", WompiWebhookApiView.as_view(), name="webhook"),
    path("wompi/redirect/", WompiRedirectTemplateView.as_view(), name="redirect"),
    path("wompi/transaction/", WompiTransactionApiView.as_view(), name="transaction"),
]
