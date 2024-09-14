from django.urls import path, include

from taewoo_apps.oauth_views import (
    NaverLoginRedirectView,
    NaverCallBackView,
    KakaoLoginRedirectView,
    KakaoCallBackView,
    GoogleLoginRedirectView,
    GoogleCallBackView,
)

urlpatterns = []

urlpatterns_api_v1 = [
    # Oauth url
    path("naver/login", NaverLoginRedirectView.as_view(), name="naver-login"),  # Naver Login
    path("naver/callback/", NaverCallBackView.as_view(), name="naver-callback"),  # Naver Callback
    path("kakao/login", KakaoLoginRedirectView.as_view(), name="kakao-login"),  # Kakao Login
    path("kakao/callback/", KakaoCallBackView.as_view(), name="naver-callback"),  # KaKao Callback
    path("google/login", GoogleLoginRedirectView.as_view(), name="google-login"),  # Google Login
    path("google/callback/", GoogleCallBackView.as_view(), name="google-callback"),  # Google Callback
]


urlpatterns += [
    path("", include((urlpatterns_api_v1, "api-oauth-v1"))),
]
