from typing import Optional

import requests
from django.conf import settings

from taewoo_apps.constants import (
    GOOGLE_CALLBACK_URL,
    GOOGLE_LOGIN_URL,
    GOOGLE_PROFILE_URL,
    GOOGLE_SCOPE,
    GOOGLE_STATE,
    GOOGLE_TOKEN_URL,
)
from taewoo_apps.services.social_login_service import SocialLoginService


class GoogleSocialLoginService(SocialLoginService):

    _client_id: Optional[str] = settings.GOOGLE_CLIENT_ID
    _secret_id: Optional[str] = settings.GOOGLE_SECRET
    _callback_url: Optional[str] = GOOGLE_CALLBACK_URL
    _state: Optional[str] = GOOGLE_STATE
    _scope: Optional[str] = GOOGLE_SCOPE
    _login_url: Optional[str] = GOOGLE_LOGIN_URL
    _token_url: Optional[str] = GOOGLE_TOKEN_URL
    _profile_url: Optional[str] = GOOGLE_PROFILE_URL

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
