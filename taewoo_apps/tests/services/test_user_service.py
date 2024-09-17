from unittest.mock import patch

from django.test import TestCase

from taewoo_apps.services.user_service import UserService
from users.models import User


class UserServiceTest(TestCase):
    def setUp(self) -> None:
        # Given
        self.user_service = UserService()
        self.email = "test@example.com"
        self.nickname = "test_nickname"
        self.password = "valid_password"
        self.phone_number = "010-1234-5678"

    def test_create_common_user_by_email(self) -> None:
        # When
        user = self.user_service.create_common_user_by_email(
            email=self.email,
            nickname=self.nickname,
            password=self.password,
            phone_number=self.phone_number,
        )

        # Then
        self.assertEqual(user.email, self.email)

    def test_activate_user(self) -> None:
        # Given
        self.user_service.create_common_user_by_email(
            email=self.email,
            nickname=self.nickname,
            password=self.password,
            phone_number=self.phone_number,
        )

        # When
        self.user_service.activate_user_by_email(email=self.email)
        user = User.get_user_by_email(email=self.email)
        # Then
        self.assertTrue(user.is_active)  # type: ignore

    def test_get_or_create_social_user_by_email_new_user(self) -> None:
        # When
        new_user = self.user_service.get_or_create_social_user_by_email(email="Test_user")

        # Then
        self.assertTrue(new_user.is_active)  # type: ignore
        self.assertEqual(new_user.email, "Test_user")  # type: ignore
