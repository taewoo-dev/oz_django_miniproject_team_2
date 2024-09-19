# authenticate -> api
from typing import TYPE_CHECKING, Any, Optional

from django.contrib.auth.base_user import BaseUserManager

if TYPE_CHECKING:
    from users.models import User


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
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)

    def create_social_user(self, email: str) -> Optional["User"]:
        if not email:
            raise ValueError("The Email field must be set")

        user = self.model(email=self.normalize_email(email))
        user.set_unusable_password()  # 소셜 로그인 사용자는 비밀번호 없음
        user.is_active = True  # 소셜 로그인 시 바로 활성화
        user.save(using=self._db)
        return user
