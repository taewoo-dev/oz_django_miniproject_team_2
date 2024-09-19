from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import oauth_naver
from users.views.home import HomeView
from users.views.signup import SignUpAPIView
from users.views.verification import EmailVerificationView

# from .views import CustomTokenRefreshView, CustomTokenVerifyView

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup"),
    path("email-verify/", EmailVerificationView.as_view(), name="email-verify"),
    # Simple JWT Authentication
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("home/", HomeView.as_view(), name="login_success"),
    # 네이버 소셜 로그인
    path("naver/login/", oauth_naver.NaverLoginView.as_view(), name="naver_login"),  # 로그인 리다이렉트
    path("naver/callback/", oauth_naver.NaverCallbackView.as_view(), name="naver_callback"),  # 로그인 콜백

]
