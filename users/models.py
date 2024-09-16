from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models

from core.models import BaseModel
from users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(("email address"), unique=True)

    nickname_validator = UnicodeUsernameValidator()
    phone_number_validator = RegexValidator(
        regex=r"010-\d{4}-\d{4}$", message="핸드폰번호는 010-xxxx-xxxx 형식으로 만들어주세요."
    )

    nickname = models.CharField(
        ("nickname"),
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text=("문자, 숫자, 특수문자( @/./+/-/_ )를 이용해 닉네임을 만들어주세요."),
        validators=[nickname_validator],
        error_messages={
            "unique": ("이미 nickname이 존재합니다."),
        },
    )
    name = models.CharField(max_length=20)
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        validators=[phone_number_validator],
    )
    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("사용자가 관리자 사이트에 로그인 할 수 있는지 지정합니다.(특정권한)"),
    )
    is_active = models.BooleanField(
        ("active"),
        default=False,
        help_text=("사용자가 활성상태로 처리될 지 여부를 지정합니다.(사용자를 삭제하지 않고 비활성화하려면 선택해제)"),
    )

    objects = CustomUserManager()

    # 로그인할 때 사용할 식별자 설정
    USERNAME_FIELD = "email"
    # 이메일 이외에 사용자 생성시 필수로 입력해야 할 필드
    REQUIRED_FIELDS = ["nickname", "name", "phone_number"]

    def __str__(self) -> str:
        return self.email

    @classmethod
    def get_user_by_email(cls, email: str) -> Optional["User"]:
        try:
            return cls.objects.get(email=email)
        except cls.DoesNotExist:
            return None
