from typing import Optional, TYPE_CHECKING

from django.contrib.auth.base_user import BaseUserManager

if TYPE_CHECKING:
    from users.models import User


class UserManger(BaseUserManager):
    def create_user(self, email: str, password: str, nickname: str) -> Optional["User"]:
        if not email:
            raise ValueError("올바른 메세지를 입력해주세요")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.nickname = nickname
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, nickname: str = "관리자") -> "User":
        user = self.create_user(email=email, password=password, nickname=nickname)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_social_user(self, email: str) -> Optional["User"]:
        if not email:
            raise ValueError("The Email field must be set")

        user = self.model(email=self.normalize_email(email))
        user.set_unusable_password()  # 소셜 로그인 사용자는 비밀번호 없음
        user.is_active = True  # 소셜 로그인 시 바로 활성화
        user.save(using=self._db)
        return user
