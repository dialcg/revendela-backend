from allauth.account.adapter import DefaultAccountAdapter
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class RoleSelectionView(LoginRequiredMixin, TemplateView):
    template_name = "account/role_selection.html"

    def post(self, request, *args, **kwargs):
        role = request.POST.get("role")
        if role in ["buyer", "seller"]:
            user = request.user
            user.role = role
            user.save()

            if role == "buyer":
                return redirect(reverse("buyer_tickets"))
            elif role == "seller":
                return redirect(reverse("seller_tickets"))
        return self.get(request, *args, **kwargs)


class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        if user.is_authenticated:
            if not user.role:
                return reverse("role_selection")
            elif user.role == "buyer":
                return reverse("buyer_tickets")
            elif user.role == "seller":
                return reverse("seller_tickets")
        return super().get_login_redirect_url(request)


class CustomSignupView(forms.Form):

    def signup(self, request, user):
        role = request.POST.get("role")
        user.role = role
        user.save()
