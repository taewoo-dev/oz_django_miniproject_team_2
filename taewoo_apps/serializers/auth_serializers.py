from typing import Any

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


# 회원가입 serializer
class UserRegistrationSerializer(serializers.ModelSerializer[User]):
    password2 = serializers.CharField(write_only=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ["email", "nickname", "password", "password2", "phone_number"]

    def validate_email(self, email: str) -> str:
        if User.get_user_by_email(email=email):
            raise serializers.ValidationError("This email is already registered.")
        return email

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if data["password"] != data["password2"]:
            raise ValidationError("비밀번호가 일치하지 않습니다")
        return data


# 로그인 serializer
class UserLoginSerializer(serializers.Serializer[Any]):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid email or password.")
            if not user.is_active:
                raise serializers.ValidationError("This account is inactive.")
        else:
            raise serializers.ValidationError("Must include both email and password.")

        data["user"] = user
        return data


# 사용자 비밀번호 변경 serializer
class PasswordChangeSerializer(serializers.Serializer):  # type: ignore
    pass


# 사용자 비밀번호 초기화 serializer
class PasswordResetSerializer(serializers.Serializer):  # type: ignore
    pass


# 유저 프로필 조회 및 수정을 위한 serializer
class UserDetailSerializer(serializers.ModelSerializer):  # type: ignore
    pass


# 관리자 또는 사용자에게 유저 목록을 제공하는 serializer
class UserListSerializer(serializers.ModelSerializer):  # type: ignore
    pass


# 유저 계정을 비활성화하는 serializer
class UserDeactivationSerializer(serializers.ModelSerializer):  # type: ignore
    pass


# 유저의 로그인 후 토큰을 발급하는 serializer
class UserTokenSerializer(serializers.Serializer):  # type: ignore
    pass
