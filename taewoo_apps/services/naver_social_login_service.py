from typing import Optional

import requests
from django.conf import settings

from taewoo_apps.constants import (
    NAVER_CALLBACK_URL,
    NAVER_LOGIN_URL,
    NAVER_PROFILE_URL,
    NAVER_SCOPE,
    NAVER_STATE,
    NAVER_TOKEN_URL,
)
from taewoo_apps.services.social_login_service import SocialLoginService


class NaverSocialLoginService(SocialLoginService):

    _client_id: Optional[str] = settings.NAVER_CLIENT_ID
    _secret_id: Optional[str] = settings.NAVER_SECRET
    _callback_url: Optional[str] = NAVER_CALLBACK_URL
    _state: Optional[str] = NAVER_STATE
    _scope: Optional[str] = NAVER_SCOPE
    _login_url: Optional[str] = NAVER_LOGIN_URL
    _token_url: Optional[str] = NAVER_TOKEN_URL
    _profile_url: Optional[str] = NAVER_PROFILE_URL

    def get_access_token(self, code: str, state: str) -> str:  # type: ignore
        params = self._generate_access_token_payload(code, state)

        response = requests.get(self._token_url or "", params=params)
        token_response = response.json()

        access_token = token_response.get("access_token")

        if not access_token:
            raise ValueError("Access token not found in the response.")

        return access_token  # type: ignore

    def _generate_access_token_payload(self, code: str, state: str) -> dict:  # type: ignore
        payload = {
            "grant_type": "authorization_code",
            "client_id": self._client_id,
            "client_secret": self._secret_id,
            "code": code,
            "state": state,
        }
        return payload
