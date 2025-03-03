from django.urls import include, path
from .views import (
    TicketSaleView,
    BuyerTicketListView,
    SellerTicketListView,
    TicketDetailView,
    TicketPurchaseView,
    TicketViewSet
)
from rest_framework.routers import DefaultRouter
from authy.views import RoleSelectionView

router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = router.urls

urlpatterns = [
    path("", TicketSaleView.as_view(), name="ticket_sale_view"),
    path("buyer-tickets/", BuyerTicketListView.as_view(), name="buyer_tickets"),
    path("seller-tickets/", SellerTicketListView.as_view(), name="seller_tickets"),
    path("accounts/role_selection/", RoleSelectionView.as_view(), name="role_selection"),
    path("tckt/<uuid:uuid>/", TicketDetailView.as_view(), name="ticket_detail"),
    path("tckt/<uuid:uuid>/purchase/", TicketPurchaseView.as_view(), name="ticket_purchase"),
    path('', include(router.urls)),
]
