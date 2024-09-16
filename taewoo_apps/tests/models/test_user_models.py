from django.db import IntegrityError
from django.test import TestCase

from users.models import User


class UserModelTestCase(TestCase):
    def setUp(self) -> None:
        # Given
        self.email = "test@example.com"
        self.password = "test_password!!"

        self.user_data = {
            "nickname": "test_nickname",
            "name": "test_name",
            "phone_number": "test_phone_number",
        }

    def test_create_user(self) -> None:
        # When: 사용자를 생성
        user = User.objects.create_user(self.email, self.password, **self.user_data)

        # Then: 생성된 사용자의 데이터와 입력한 데이터가 같은지 비교
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(user.nickname, self.user_data["nickname"])
        self.assertEqual(user.name, self.user_data["name"])
        self.assertEqual(user.phone_number, self.user_data["phone_number"])

    def test_create_superuser(self) -> None:
        # When
        super_user = User.objects.create_superuser(email=self.email, password=self.password, **self.user_data)
        # Then
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)

    def test_create_user_is_not_superuser(self) -> None:
        # When
        user = User.objects.create_user(self.email, self.password, **self.user_data)

        # Then
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_user_without_email_raises_error(self) -> None:
        # Expect
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password=self.password)  # type: ignore

    def test_create_user_without_password_raises_error(self) -> None:
        # Expect
        with self.assertRaises(ValueError):
            User.objects.create_user(email=self.email, password=None)

    def test_password_is_hashed(self) -> None:
        # When
        user = User.objects.create_user(self.email, self.password, **self.user_data)

        # Then
        self.assertNotEqual(user.password, self.password)
        self.assertTrue(user.check_password(self.password))

    def test_email_must_be_unique(self) -> None:
        # Expect
        User.objects.create_user(self.email, self.password, **self.user_data)

        with self.assertRaises(IntegrityError):
            User.objects.create_user(self.email, self.password, **self.user_data)

    def test_email_is_normalized(self) -> None:
        # When
        user = User.objects.create_user(email="test@Example.com", password=self.password)

        # Then
        self.assertEqual(user.email, self.email)
