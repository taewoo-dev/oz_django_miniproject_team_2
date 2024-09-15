from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views.signup import SignUpAPIView
from .views.verification import EmailVerificationView

# from .views import CustomTokenRefreshView, CustomTokenVerifyView

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup"),
    path("email-verify/", EmailVerificationView.as_view(), name="email-verify"),
    # Simple JWT Authentication
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
