from unittest.mock import MagicMock, patch

from django.test import TestCase

from taewoo_apps.services.token_service import TokenService
from users.models import User


class TokenServiceTest(TestCase):
    def setUp(self) -> None:
        self.token_service = TokenService()

        self.email = "test@example.com"
        self.nickname = "test_nickname"
        self.password = "valid_password"
        self.phone_number = "010-1234-5678"

        self.user = User.objects.create_user(
            email=self.email,
            nickname=self.nickname,
            password=self.password,
            phone_number=self.phone_number,
        )

    @patch("taewoo_apps.services.token_service.RefreshToken.for_user")
    def test_generate_jwt_token(self, mock_for_user: MagicMock) -> None:
        # Given
        mock_refresh_token = mock_for_user.return_value
        mock_refresh_token.access_token = "mock_access_token"
        mock_refresh_token.__str__.return_value = "mock_refresh_token"

        # When
        access_token, refresh_token = self.token_service.generate_jwt_token(self.user)

        # Then
        mock_for_user.assert_called_once_with(self.user)
        self.assertEqual(access_token, "mock_access_token")
        self.assertEqual(refresh_token, "mock_refresh_token")

    @patch("taewoo_apps.services.token_service.RefreshToken")
    def test_blacklist_refresh_token(self, mock_refresh_token: MagicMock) -> None:
        # Given
        mock_token_instance = mock_refresh_token.return_value

        # When
        self.token_service.blacklist_refresh_token("mock_refresh_token")

        # Then
        mock_refresh_token.assert_called_once_with("mock_refresh_token")
        mock_token_instance.blacklist.assert_called_once()
