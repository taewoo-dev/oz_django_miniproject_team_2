from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Account(models.Model):

    BANK_CODE_CHOICES = [
        ("088", "신한은행"),
        ("002", "산업은행"),
        ("003", "기업은행"),
        ("004", "국민은행"),
        ("005", "외환은행"),
        # 기타 은행 코드 추가 가능
        # 배포 전에 뱅크 코드 파일 작성하여 관리 필요
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="계좌주")
    account_number = models.CharField("계좌번호", max_length=20)
    bank_code = models.CharField("은행코드", max_length=10, choices=BANK_CODE_CHOICES)
    account_type = models.CharField("계좌종류", max_length=20)
    balance = models.PositiveIntegerField("잔액")

    def __str__(self) -> str:
        return f"{self.bank_code} - {self.account_number}"
