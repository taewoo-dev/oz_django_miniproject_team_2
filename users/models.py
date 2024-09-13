from typing import Any, Optional

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models


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


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(("email address"), unique=True)

    nickname_validator = UnicodeUsernameValidator()
    phone_number_validator = RegexValidator(
        regex=r"010-\d{4}-\d{4}$", message="핸드폰번호는 010-xxxx-xxxx 형식으로 만들어주세요."
    )

    nickname = models.CharField(
        ("nickname"),
        max_length=100,
        unique=True,
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

    # def email_user(self, subject: str, message: str, from_email: str=None, **kwargs) ->None:
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


#
# class Account(models.Model):
#     BANK_CODE_CHOICES: list[tuple[str, str]] = [
#         ('090', '카카오뱅크'),
#         ('KB', 'Kookmin Bank'),
#         ('NH', 'Nonghyup Bank'),
#         ('IBK','Industrial Bank'),
#         ('KEB', 'Hana Bank'),
#     ]
#     ACCOUNT_TYPE_CHOICES: list[tuple[str, str]] = [
#         ('CHECKING', 'Checking Account'),
#         ('DEPOSIT', 'Deposit Account'),
#         ('SAVINGS', 'Savings Account'),
#         ('OVERDRAFT', 'Overdraft Account'),
#         ('LOAN', 'Loan Account'),
#         ('CMA', 'Cash Management Account'),
#     ]
#     user_id: User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account')
#     account_number: str = models.CharField(max_length=30, unique=True)
#     bank_code: str = models.CharField(max_length=10, choices=BANK_CODE_CHOICES)
#     account_type: str = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
#     balance: int = models.PositiveIntegerField(default=0)
#
#     def __str__(self) -> str:
#         return  f"{self.account_id} - {self.transaction_type} - {self.transaction_amount}"
#
#
# class Transaction_history(models.Model):
#     TRANSACTION_TYPE_CHOICES: list[tuple[str, str]] = [
#         ('DEPOSIT', 'Deposit Transaction'),
#         ('WITHDRAW', 'Withdraw Transaction'),
#     ]
#     PAYMENT_METHOD_CHOICES: list[tuple[str, str]] = [
#         ('CASH', 'Cash'),
#         ('CREDIT', 'Credit Card Payment'),
#         ('BANK', 'Bank Transfer'),
#         ('AUTOMATIC', 'Automatic Transfer'),
#     ]
#
#     account_id: Account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transaction_history')
#     transaction_amount: int = models.IntegerField(default=0)
#     transaction_balance: int = models.IntegerField(default=0)
#     transaction_description: str = models.TextField(blank=True)
#     transaction_type: str = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
#     payment_method: str = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
#     transaction_datetime = models.DateTimeField(auto_now=True)
#
#     def __str__(self) -> str:
#         return f"{self.account_id} - {self.transaction_type} - {self.transaction_amount}"
