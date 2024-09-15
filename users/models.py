from typing import Any, Optional

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models

from core.models import BaseModel


# authenticate -> api
class CustomUserManager(BaseUserManager["User"]):
    # **extra_fields는 사용자 모델에 있는 다른 필드들을 처리하는 역할을 함.
    def create_user(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> "User":
        if not email:
            raise ValueError("이메일 주소를 입력해야 합니다.")
        if password is None:
            raise ValueError("비밀번호를 반드시 설정해야 합니다.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 해시화
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


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
        validators=[phone_number_validator],
    )
    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("사용자가 관리자 사이트에 로그인 할 수 있는지 지정합니다.(특정권한)"),
    )
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=("사용자가 활성상태로 처리될 지 여부를 지정합니다.(사용자를 삭제하지 않고 비활성화하려면 선택해제)"),
    )

    objects = CustomUserManager()

    # 로그인할 때 사용할 식별자 설정
    USERNAME_FIELD = "email"
    # 이메일 이외에 사용자 생성시 필수로 입력해야 할 필드
    REQUIRED_FIELDS = ["nickname", "name", "phone_number"]

    def __str__(self) -> str:
        return self.email
