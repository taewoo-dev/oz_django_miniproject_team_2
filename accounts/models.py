from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

from accounts.constants import ACCOUNT_TYPE_CHOICES, BANK_CODE_CHOICES
from core.models import BaseModel

User = get_user_model()


class Account(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="계좌주")
    account_number = models.CharField("계좌번호", max_length=20, unique=True)
    bank_code = models.CharField("은행코드", max_length=10, choices=BANK_CODE_CHOICES)
    account_type = models.CharField("계좌종류", max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    balance = models.DecimalField("잔액", max_digits=15, decimal_places=2, default=Decimal("0.00"))

    def __str__(self) -> str:
        return f"{self.bank_code} - {self.account_number}"
