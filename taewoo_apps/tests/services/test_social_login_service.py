from typing import Any, Optional
from unittest.mock import MagicMock, patch
from urllib.parse import urlencode

from django.test import TestCase

from taewoo_apps.services.social_login_service import SocialLoginService


class TestSocialLoginService(SocialLoginService):
    _client_id = "test_client_id"
    _callback_url = "http://localhost/callback"
    _state = "test_state"
    _scope = "profile"
    _login_url = "http://test_login_url"
    _profile_url = "http://test_profile_url"

    def get_access_token(self, *args: Any, **kwargs: Any) -> Any:
        pass

    def _generate_access_token_payload(self, *args: Any, **kwargs: Any) -> Any:
        pass


class SocialLoginServiceTest(TestCase):
    def setUp(self) -> None:
        self.service = TestSocialLoginService()

    def test_generate_login_url(self) -> None:
        # Given
        params = {
            "response_type": "code",
            "client_id": "test_client_id",
            "redirect_uri": "http://localhost/callback",
            "state": self.service.signed_state,
            "scope": "profile",
        }
        encode_data = urlencode(params)

        # When
        login_url = self.service.generate_login_url()

        # Then
        self.assertIn(encode_data, login_url)

    @patch("taewoo_apps.services.social_login_service.requests.get")
    def test_get_profile_json(self, mock_get: MagicMock) -> None:
        # Given
        mock_response = MagicMock()
        mock_response.json.return_value = {"email": "test@example.com"}
        mock_get.return_value = mock_response

        # When
        profile_data = self.service.get_profile_json(access_token="mock_access_token")

        # Then
        mock_get.assert_called_once_with(
            "http://test_profile_url",
            headers={"Authorization": "Bearer mock_access_token"},
        )
        self.assertEqual(profile_data, {"email": "test@example.com"})
