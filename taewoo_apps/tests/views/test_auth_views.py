from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserRegistrationAPITest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("api-v1:api-auth-v1:user-register")
        self.user_data = {
            "email": "test_email@naver.com",
            "nickname": "test_nickname",
            "password": "test_password",
            "password2": "test_password",
            "phone_number": "010-1234-1234",
        }

    def test_registration_success(self) -> None:
        # When
        response = self.client.post(self.url, self.user_data, format="json")
        response_data = {
            "success": True,
            "message": "User registered successfully.",
        }

        # Then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, response_data)

    def test_password_mismatch(self) -> None:
        # Given
        invalid_data = self.user_data.copy()
        invalid_data["password2"] = "test_password22"

        # When
        response = self.client.post(self.url, invalid_data, format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
