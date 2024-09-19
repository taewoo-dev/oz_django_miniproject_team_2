from django.db import models

from accounts.models import Account
from core.models import BaseModel
from transaction_historys.constants import (
    PAYMENT_TYPE_CHOICES,
    TRANSACTION_TYPE_CHOICES,
)


class TransactionHistory(BaseModel):

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_amount = models.PositiveIntegerField()  # 양수만 받게
    transaction_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # 소수점 두자리
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    transaction_description = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f"Transaction {self.pk} on Account {self.account.account_number}"

