from typing import Any, Dict

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.crypto import get_random_string
from prompt_toolkit.validation import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 시리얼라이저->데이터의 검증과 변환을 처리하는 역할

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):  # type: ignore
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password2", "nickname", "phone_number"]

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")

        if not data.get("phone_number"):
            raise serializers.ValidationError("전화번호는 필수 입력 하셔야합니다.")
        return data

    def create(self, validated_data: Dict[str, Any]) -> Any:
        if not validated_data["nickname"]:
            random_suffix = get_random_string(8)
            validated_data["nickname"] = f"user{random_suffix}"

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            nickname=validated_data["nickname"],
            phone_number=validated_data["phone_number"],
        )

        user.is_active = False  # 이메일 인증 후 활성화
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("이메일 또는 비밀번호가 올바르지 않습니다.")

        # 인증된 사용자는 리턴
        data["user"] = user
        return data


# 추가적인 사용자 정보를 JWT 토큰에 포함시키기 위한 커스텀 시리얼라이저(토큰에 사용자 정보 추가할 수 있음)
# 이거쓰면 view에서 CustomTokenObtainPairView 클래스 만들어서 TokenObtainPairSeializer 상속받아야함
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['nickcname'] = user.nickname  # 유저의 이름을 토큰에 추가
#         # 여기에 더 많은 커스텀 클레임을 추가할 수 있음
#         # 예시: token['role'] = user.role
#
#         return token
