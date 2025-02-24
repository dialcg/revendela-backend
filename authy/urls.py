from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import SimpleRouter
from .views import LogoutView, UserProfileViewSet

router = SimpleRouter()
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/logout/", LogoutView.as_view(), name="token_logout"),
    path('', include(router.urls)),
]
