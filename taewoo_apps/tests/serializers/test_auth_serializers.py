from django.contrib.auth import authenticate
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from taewoo_apps.serializers.auth_serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
)
from users.models import User


class UserRegistrationSerializerTest(TestCase):
    def setUp(self) -> None:
        # Given
        self.data = {
            "email": "test@example.com",
            "password": "valid_password",
            "password2": "valid_password",
            "nickname": "test_nickname",
            "phone_number": "010-1234-5678",
        }

    def test_valid_data(self) -> None:
        # Given
        serializer = UserRegistrationSerializer(data=self.data)

        # When
        is_valid = serializer.is_valid()

        # Then
        self.assertTrue(is_valid)
        self.assertEqual(serializer.validated_data["email"], self.data["email"])

    def test_duplicate_email(self) -> None:
        # Given
        serializer = UserRegistrationSerializer(data=self.data)
        user = User.objects.create_user(
            email="test@example.com",
            password="valid_password",
            nickname="existing_nickname",
            phone_number="010-8765-4321",
        )

        # Expect
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_form_emali(self) -> None:
        # Given
        invalid_data_with_email = self.data.copy()
        invalid_data_with_email["email"] = "test"
        serializer = UserRegistrationSerializer(data=invalid_data_with_email)

        # Expect
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_password_mismatch(self) -> None:
        # Given
        invalid_data = self.data.copy()
        invalid_data["password2"] = "invalid_password"
        serializer = UserRegistrationSerializer(data=invalid_data)

        # Except

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class UserLoginSerializerTest(TestCase):
    def setUp(self) -> None:
        # Given
        self.user = User.objects.create_user(
            email="test@example.com",
            password="qwerasd!!",
            nickname="existing_nickname",
            phone_number="010-1234-1234",
            is_active=True,  # 유저 생성 시 활성화 상태로 생성
        )

        self.inactive_user = User.objects.create_user(
            email="test2@example.com",
            password="qwerasd!!",  # 비밀번호는 create_user로 암호화됨
            nickname="existing_nickname2",
            phone_number="010-1234-1235",
        )

    def test_missing_email(self) -> None:
        # Given
        invalid_data = {
            "email": "test_email",
            "password": "",
        }
        serializer = UserLoginSerializer(data=invalid_data)

        # Except
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_missing_password(self) -> None:
        # Given
        invalid_data = {
            "email": "",
            "password": "qwerasd!!",
        }
        serializer = UserLoginSerializer(data=invalid_data)

        # Except
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_user_does_not_exist(self) -> None:
        # Given
        invalid_data = {
            "email": "test_not@example.com",
            "password": "qwerasd!!",
        }
        serializer = UserLoginSerializer(data=invalid_data)

        # Except
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_user_exist(self) -> None:
        # Given
        valid_data = {
            "email": "test@example.com",
            "password": "qwerasd!!",
        }
        serializer = UserLoginSerializer(data=valid_data)

        # When
        is_valid = serializer.is_valid(raise_exception=True)

        # Then
        self.assertTrue(is_valid)
        self.assertEqual(serializer.validated_data["user"], self.user)

    def test_inactive_user(self) -> None:
        # Given
        valid_data = {
            "email": "test2@example.com",
            "password": "qwerasd!!",
        }
        serializer = UserLoginSerializer(data=valid_data)

        # Except
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
