from abc import ABC, abstractmethod
from typing import Any, Optional
from urllib.parse import urlencode

import requests
from django.core import signing


class SocialLoginService(ABC):

    _client_id: Optional[str]
    _secret_id: Optional[str]
    _callback_url: Optional[str]
    _state: Optional[str]
    _scope: Optional[str]
    _login_url: Optional[str]
    _token_url: Optional[str]
    _profile_url: Optional[str]

    @property
    def signed_state(self) -> str:
        return signing.dumps(self._state)

    def generate_login_url(self) -> str:
        params = self._generate_login_params()
        return self._create_login_url(params)

    def _generate_login_params(self) -> dict[str, Any]:
        return {
            "response_type": "code",
            "client_id": self._client_id,
            "redirect_uri": self._callback_url,
            "state": self.signed_state,
            "scope": self._scope,
        }

    def _create_login_url(self, params: dict[str, str]) -> str:
        return f"{self._login_url}?{urlencode(params)}"

    @abstractmethod
    def get_access_token(self, *args: Any, **kwargs: Any) -> Any: ...

    @abstractmethod
    def _generate_access_token_payload(self, *args: Any, **kwargs: Any) -> Any: ...

    def get_profile_json(self, access_token: str) -> dict[str, Any]:
        headers = self._generate_auth_headers(access_token)

        response = requests.get(self._profile_url or "", headers=headers)

        return response.json()  # type: ignore

    def _generate_auth_headers(self, access_token: str) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        return headers
