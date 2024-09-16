from django.core import signing
from rest_framework.exceptions import ValidationError
from django.test import TestCase

from taewoo_apps.constants import NAVER_STATE, KAKAO_STATE, GOOGLE_STATE
from taewoo_apps.serializers.oauth_serializer import (
    NaverCallBackSerializer,
    KakaoCallBackSerializer,
    GoogleCallBackSerializer,
)


class SocialCallBackSerializerTest(TestCase):
    def test_naver_callback_serializer(self) -> None:
        # 유효한 state 테스트
        self._test_valid_state(NaverCallBackSerializer, NAVER_STATE)

        # 잘못된 state 테스트
        self._test_invalid_state(NaverCallBackSerializer)

    def test_kakao_callback_serializer(self) -> None:
        # 유효한 state 테스트
        self._test_valid_state(KakaoCallBackSerializer, KAKAO_STATE)

        # 잘못된 state 테스트
        self._test_invalid_state(KakaoCallBackSerializer)

    def test_google_callback_serializer(self) -> None:
        # 유효한 state 테스트
        self._test_valid_state(GoogleCallBackSerializer, GOOGLE_STATE)

        # 잘못된 state 테스트
        self._test_invalid_state(GoogleCallBackSerializer)

    def _test_valid_state(self, serializer_class, expected_state: str) -> None:
        # Given
        state = signing.dumps(expected_state)
        valid_data = {
            "code": "valid_code",
            "state": state,
        }

        # When
        serializer = serializer_class(data=valid_data)
        is_valid = serializer.is_valid()

        # Then
        self.assertTrue(is_valid)

    def _test_invalid_state(self, serializer_class) -> None:
        # Given
        invalid_state = signing.dumps("wrong_state")  # 잘못된 state 값
        invalid_data = {
            "code": "valid_code",
            "state": invalid_state,
        }

        # When
        serializer = serializer_class(data=invalid_data)

        # Then
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
