from unittest.mock import MagicMock, patch

from django.test import TestCase

from taewoo_apps.services.kakao_social_login_service import KakaoSocialLoginService


class TestKakaoSocialLoginService(TestCase):
    def setUp(self) -> None:
        self.kakao_service = KakaoSocialLoginService()
        self.code = "test_code"
        self.access_token = "mock_access_token"

    @patch("requests.post")
    def test_get_access_token_success(self, mock_post: MagicMock) -> None:
        # Given
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": self.access_token}
        mock_post.return_value = mock_response

        # When
        access_token = self.kakao_service.get_access_token(self.code)

        # Then
        self.assertEqual(access_token, self.access_token)
        mock_post.assert_called_once_with(
            self.kakao_service._token_url,
            data={
                "grant_type": "authorization_code",
                "client_id": self.kakao_service._client_id,
                "client_secret": self.kakao_service._secret_id,
                "code": self.code,
                "redirect_uri": self.kakao_service._callback_url,
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
            self.kakao_service.get_access_token(self.code)

        self.assertEqual(str(exc.exception), "Access token not found in the response.")
        mock_post.assert_called_once_with(
            self.kakao_service._token_url,
            data={
                "grant_type": "authorization_code",
                "client_id": self.kakao_service._client_id,
                "client_secret": self.kakao_service._secret_id,
                "code": self.code,
                "redirect_uri": self.kakao_service._callback_url,
            },
        )

    def test_generate_access_token_payload(self) -> None:
        # When
        payload = self.kakao_service._generate_access_token_payload(self.code)

        # Then
        expected_payload = {
            "grant_type": "authorization_code",
            "client_id": self.kakao_service._client_id,
            "client_secret": self.kakao_service._secret_id,
            "code": self.code,
            "redirect_uri": self.kakao_service._callback_url,
        }
        self.assertEqual(payload, expected_payload)
