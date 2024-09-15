from typing import Optional

import requests
from django.conf import settings

from taewoo_apps.constants import (
    KAKAO_CALLBACK_URL,
    KAKAO_LOGIN_URL,
    KAKAO_PROFILE_URL,
    KAKAO_SCOPE,
    KAKAO_STATE,
    KAKAO_TOKEN_URL,
)
from taewoo_apps.services.social_login_service import SocialLoginService


class KakaoSocialLoginService(SocialLoginService):

    _client_id: Optional[str] = settings.KAKAO_CLIENT_ID
    _secret_id: Optional[str] = settings.KAKAO_SECRET
    _callback_url: Optional[str] = KAKAO_CALLBACK_URL
    _state: Optional[str] = KAKAO_STATE
    _scope: Optional[str] = KAKAO_SCOPE
    _login_url: Optional[str] = KAKAO_LOGIN_URL
    _token_url: Optional[str] = KAKAO_TOKEN_URL
    _profile_url: Optional[str] = KAKAO_PROFILE_URL

    def get_access_token(self, code: str) -> str:  # type: ignore
        payload = self._generate_access_token_payload(code)

        response = requests.post(self._token_url or "", data=payload)
        token_response = response.json()

        access_token = token_response.get("access_token")

        if not access_token:
            raise ValueError("Access token not found in the response.")

        return access_token  # type: ignore

    def _generate_access_token_payload(self, code: str) -> dict:  # type: ignore
        payload = {
            "grant_type": "authorization_code",
            "client_id": self._client_id,
            "client_secret": self._secret_id,
            "code": code,
            "redirect_uri": self._callback_url,
        }
        return payload
