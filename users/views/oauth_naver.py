import urllib.parse

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.views import APIView

from config.local import NAVER_CLIENT_ID, NAVER_SECRET
from users.constants import NAVER_CALLBACK_URL, NAVER_STATE, NAVER_LOGIN_URL, NAVER_TOKEN_URL, NAVER_PROFILE_URL

User = get_user_model()

# NAVER_CALLBACK_URL = '/naver/callback/'
# NAVER_STATE = 'naver_login'
# NAVER_LOGIN_URL = 'https://nid.naver.com/oauth2.0/authorize'
# NAVER_TOKEN_URL = 'http://nid.naver.com/oauth2.0/token'
# NAVER_PROFILE_URL = 'http://openapi.naver.com/v1/nid/me'


class NaverLoginView(APIView):
    queryset = User.objects.all()

    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get(self, request):
        client_id = settings.NAVER_CLIENT_ID
        redirect_uri = request.build_absolute_uri(NAVER_CALLBACK_URL)  # 절대 경로로 콜백 URI 설정
        state = NAVER_STATE

        params = {"response_type": "code", "client_id": client_id, "redirect_uri": redirect_uri, "state": state}

        naver_login_url = f"{NAVER_LOGIN_URL}?{urllib.parse.urlencode(params)}"
        return redirect(naver_login_url)


class NaverCallbackView(APIView):
    def get(self, request):
        code = request.GET.get("code")
        state = request.GET.get("state")
        client_id = NAVER_CLIENT_ID
        client_secret = NAVER_SECRET
        redirect_uri = request.build_absolute_uri(NAVER_CALLBACK_URL)

        token_url = NAVER_TOKEN_URL
        token_data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "state": state,
        }

        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()

        if "access_token" not in token_json:
            return render(request, "users/naver_failute.html", {"error": "access_token을 제대로 받아오지 못했습니다."})

        access_token = token_json["access_token"]

        # 네이버 사용자 프로필 요청
        profile_url = NAVER_PROFILE_URL
        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        profile_response = requests.get(profile_url, headers=headers)
        profile_json = profile_response.json()

        if "response" not in profile_json:
            return render(request, "users/naver_failure.html", {"error": "사용자 프로필 정보를 가져오지 못했습니다."})

        naver_user_info = profile_json["response"]

        # 사용자 정보 처리
        user, created = User.objects.get_or_create(
            username=naver_user_info["id"],  # 네이버의 고유 ID로 사용자 식별
            defaults={
                "email": naver_user_info.get("email"),
                "nickname": naver_user_info.get("nickname"),
            },
        )
        login(request, user)
        return redirect("login_success")  # Simple JWT로그인 리다이렉션 경로와 동일
