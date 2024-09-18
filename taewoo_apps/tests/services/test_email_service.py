from unittest.mock import MagicMock, patch

from django.conf import settings
from django.core import signing
from django.test import TestCase

from taewoo_apps.constants import VERIFY_EMAIL_URL
from taewoo_apps.services.email_service import EmailService


class EmailServiceTest(TestCase):
    def setUp(self) -> None:
        # Given
        self.email_service = EmailService()
        self.email = "test@example.com"

    def test_create_signed_email_token(self) -> None:
        # When
        token = self.email_service.create_signed_email_token(email=self.email)
        decoded_token = signing.loads(token)
        signed_email = self.email_service.signer.sign(self.email)

        # Then
        self.assertTrue(token)
        self.assertEqual(decoded_token, signed_email)

    def test_validate_email_token_expired(self) -> None:
        # When
        token = self.email_service.create_signed_email_token(self.email)
        validate_email = self.email_service.validate_email_token(token)

        # Then
        self.assertEqual(self.email, validate_email)

    def test_get_verification_email_content(self) -> None:
        # Given
        token = "test_token"

        # When
        subject, message = self.email_service.get_verification_email_content(token)

        # Then
        self.assertEqual(subject, "이메일 인증을 완료해주세요")
        self.assertIn(VERIFY_EMAIL_URL + token, message)

    @patch("taewoo_apps.services.email_service.send_mail")  # send_mail 함수를 모킹
    def test_send_email(self, mock_send_mail: MagicMock) -> None:
        # Given
        subject = "Test Subject"
        message = "Test Message"
        to_email = self.email

        # When
        self.email_service.send_email(subject, message, to_email)

        # Then
        mock_send_mail.assert_called_once_with(subject, message, settings.EMAIL_HOST_USER, [to_email])
