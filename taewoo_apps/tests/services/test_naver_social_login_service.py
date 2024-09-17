from unittest.mock import MagicMock, patch

from django.test import TestCase

from taewoo_apps.services.naver_social_login_service import NaverSocialLoginService


class TestNaverSocialLoginService(TestCase):
    def setUp(self) -> None:
        self.naver_service = NaverSocialLoginService()
        self.code = "test_code"
        self.state = "test_state"
        self.access_token = "mock_access_token"

    @patch("requests.get")
    def test_get_access_token_success(self, mock_get: MagicMock) -> None:
        # Given
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": self.access_token}
        mock_get.return_value = mock_response

        # When
        access_token = self.naver_service.get_access_token(self.code, self.state)

        # Then
        self.assertEqual(access_token, self.access_token)
        mock_get.assert_called_once_with(
            self.naver_service._token_url,
            params={
                "grant_type": "authorization_code",
                "client_id": self.naver_service._client_id,
                "client_secret": self.naver_service._secret_id,
                "code": self.code,
                "state": self.state,
            },
        )

    @patch("requests.get")
    def test_get_access_token_failure(self, mock_get: MagicMock) -> None:
        # Given
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        # When / Then and Expect
        with self.assertRaises(ValueError) as exc:
            self.naver_service.get_access_token(self.code, self.state)

        self.assertEqual(str(exc.exception), "Access token not found in the response.")
        mock_get.assert_called_once_with(
            self.naver_service._token_url,
            params={
                "grant_type": "authorization_code",
                "client_id": self.naver_service._client_id,
                "client_secret": self.naver_service._secret_id,
                "code": self.code,
                "state": self.state,
            },
        )

    def test_generate_access_token_payload(self) -> None:
        # When
        payload = self.naver_service._generate_access_token_payload(self.code, self.state)

        # Then
        expected_payload = {
            "grant_type": "authorization_code",
            "client_id": self.naver_service._client_id,
            "client_secret": self.naver_service._secret_id,
            "code": self.code,
            "state": self.state,
        }
        self.assertEqual(payload, expected_payload)
