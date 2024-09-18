from unittest.mock import MagicMock, patch

from django.test import TestCase

from taewoo_apps.services.google_social_login_service import GoogleSocialLoginService


class TestGoogleSocialLoginService(TestCase):
    def setUp(self) -> None:
        self.google_service = GoogleSocialLoginService()
        self.code = "test_code"
        self.access_token = "mock_access_token"

    @patch("requests.post")
    def test_get_access_token_success(self, mock_post: MagicMock) -> None:
        # Given
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": self.access_token}
        mock_post.return_value = mock_response

        # When
        access_token = self.google_service.get_access_token(self.code)

        # Then
        self.assertEqual(access_token, self.access_token)
        mock_post.assert_called_once_with(
            self.google_service._token_url,
            data={
                "grant_type": "authorization_code",
                "client_id": self.google_service._client_id,
                "client_secret": self.google_service._secret_id,
                "code": self.code,
                "redirect_uri": self.google_service._callback_url,
            },
        )

    @patch("requests.post")
    def test_get_access_token_failure(self, mock_post: MagicMock) -> None:
        # Given
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        # When / Then and Expect
        with self.assertRaises(ValueError) as exc:
            self.google_service.get_access_token(self.code)

        self.assertEqual(str(exc.exception), "Access token not found in the response.")
        mock_post.assert_called_once_with(
            self.google_service._token_url,
            data={
                "grant_type": "authorization_code",
                "client_id": self.google_service._client_id,
                "client_secret": self.google_service._secret_id,
                "code": self.code,
                "redirect_uri": self.google_service._callback_url,
            },
        )

    def test_generate_access_token_payload(self) -> None:
        # When
        payload = self.google_service._generate_access_token_payload(self.code)

        # Then
        expected_payload = {
            "grant_type": "authorization_code",
            "client_id": self.google_service._client_id,
            "client_secret": self.google_service._secret_id,
            "code": self.code,
            "redirect_uri": self.google_service._callback_url,
        }
        self.assertEqual(payload, expected_payload)
