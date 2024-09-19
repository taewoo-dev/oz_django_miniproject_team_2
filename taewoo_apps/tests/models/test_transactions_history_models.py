from datetime import datetime, timedelta

from django.db import IntegrityError
from django.test import TestCase

from accounts.models import Account
from transaction_historys.models import TransactionHistory
from users.models import User


class TransactionHistoryModelTestCase(TestCase):
    def setUp(self) -> None:
        # Given
        self.user = User.objects.create_user(
            email="test@example.com",
            password="test_password",
            nickname="test_nickname",
            name="test_name",
            phone_number="010-1234-5678",
        )
        self.account = Account.objects.create(
            user=self.user,
            account_number="12345678901234567890",
            bank_code="088",  # 신한은행 코드
            account_type="예금",
            balance=1000000,  # 초기 잔액
        )
        # Given: 트랜잭션 데이터를 설정
        self.transaction_data = {
            "account": self.account,
            "transaction_amount": 1000,  # 트랜잭션 금액
            "transaction_balance": 1001000.00,  # 거래 후 잔액
            "transaction_type": "deposit",  # 입금
            "payment_method": "Bank",  # 결제 방법
            "transaction_description": "Initial deposit",  # 설명
        }

    def test_create_transaction_history(self) -> None:
        # When
        transaction_history = TransactionHistory.objects.create(**self.transaction_data)

        # Then
        self.assertEqual(transaction_history.account, self.transaction_data["account"])
        self.assertEqual(transaction_history.transaction_amount, self.transaction_data["transaction_amount"])
        self.assertEqual(transaction_history.transaction_balance, self.transaction_data["transaction_balance"])
        self.assertEqual(transaction_history.transaction_type, self.transaction_data["transaction_type"])
        self.assertEqual(transaction_history.payment_method, self.transaction_data["payment_method"])
        self.assertEqual(transaction_history.transaction_description, self.transaction_data["transaction_description"])

    def test_account_requires_user(self) -> None:
        # Except
        transaction_data_without_account = self.transaction_data.copy()
        transaction_data_without_account.pop("account")

        with self.assertRaises(IntegrityError):
            TransactionHistory.objects.create(**transaction_data_without_account)

    def test_transaction_amount_must_be_positive(self) -> None:
        # Except
        negative_amount = -10000
        transaction_data_with_negative_amount = self.transaction_data.copy()
        transaction_data_with_negative_amount["transaction_amount"] = negative_amount

        with self.assertRaises(IntegrityError):
            TransactionHistory.objects.create(**transaction_data_with_negative_amount)

    def test_transaction_description_optional(self) -> None:
        # When
        transaction_data_without_description = self.transaction_data.copy()
        transaction_data_without_description.pop("transaction_description")
        transaction = TransactionHistory.objects.create(**transaction_data_without_description)

        # Then
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.transaction_description, "")

    def test_transaction_history_str_representation(self) -> None:
        # When
        transaction = TransactionHistory.objects.create(**self.transaction_data)

        # Then
        expected_str = f"Transaction {transaction.pk} on Account {transaction.account.account_number}"
        self.assertEqual(str(transaction), expected_str)

    def test_transaction_history_foreign_key_account(self) -> None:
        # When
        transaction = TransactionHistory.objects.create(**self.transaction_data)

        # Then
        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.account.account_number, self.account.account_number)

    # transaction_balance 필드가 소수점 두 자리를 허용하는지 테스트 -> 이건 시리얼라이저에서 해보기
    # transaction_type 필드에서 허용되지 않은 값을 입력하면 예외가 발생하는지 테스트
    # payment_method 필드에서 허용되지 않은 값을 입력하면 예외가 발생하는지 테스트
