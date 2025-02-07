from django.urls import path
from .views import (
    TicketSaleView,
    BuyerTicketListView,
    SellerTicketListView,
    TicketDetailView,
    TicketPurchaseView,
)
from authy.views import RoleSelectionView

urlpatterns = [
    path("", TicketSaleView.as_view(), name="ticket_sale_view"),
    path("buyer-tickets/", BuyerTicketListView.as_view(), name="buyer_tickets"),
    path("seller-tickets/", SellerTicketListView.as_view(), name="seller_tickets"),
    path(
        "accounts/role_selection/", RoleSelectionView.as_view(), name="role_selection"
    ),
    path("ticket/<uuid:uuid>/", TicketDetailView.as_view(), name="ticket_detail"),
    path(
        "ticket/<uuid:uuid>/purchase/",
        TicketPurchaseView.as_view(),
        name="ticket_purchase",
    ),
]
