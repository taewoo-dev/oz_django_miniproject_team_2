from django.db import DataError, IntegrityError
from django.test import TestCase

from accounts.models import Account
from users.models import User


class AccountModelTestCase(TestCase):
    def setUp(self) -> None:
        # Given
        self.user = User.objects.create_user(
            email="test@example.com",
            password="test_password",
            nickname="test_nickname",
            name="test_name",
            phone_number="010-1234-5678",
        )

        self.account_data = {
            "user": self.user,
            "account_number": "12345678901234567890",
            "bank_code": "088",
            "account_type": "예금",
            "balance": 1000000,
        }

    def test_create_account(self) -> None:
        # When
        account = Account.objects.create(**self.account_data)

        # Then
        self.assertEqual(account.user, self.account_data["user"])
        self.assertEqual(account.account_number, self.account_data["account_number"])
        self.assertEqual(account.bank_code, self.account_data["bank_code"])
        self.assertEqual(account.account_type, self.account_data["account_type"])
        self.assertEqual(account.balance, self.account_data["balance"])

    def test_account_str_representation(self) -> None:
        # When
        account = Account.objects.create(**self.account_data)
        excepted_str = f"{account.bank_code} - {account.account_number}"
        # Then
        self.assertEqual(str(account), excepted_str)

    def test_account_requires_user(self) -> None:
        # Except
        account_data_without_user = self.account_data.copy()
        account_data_without_user.pop("user")

        with self.assertRaises(IntegrityError):
            Account.objects.create(**account_data_without_user)

    def test_account_number_max_length(self) -> None:
        # Except
        long_account_number = "1" * 25
        account_data_with_long_number = self.account_data.copy()
        account_data_with_long_number["account_number"] = long_account_number

        with self.assertRaises(DataError):
            Account.objects.create(**account_data_with_long_number)

    def test_balance_must_be_positive(self) -> None:
        # Except
        negative_balance = -10000
        account_data_with_negative_balance = self.account_data.copy()
        account_data_with_negative_balance["balance"] = negative_balance

        with self.assertRaises(IntegrityError):
            Account.objects.create(**account_data_with_negative_balance)

    def test_account_type_max_length(self) -> None:
        # Except
        long_account_type = "1" * 25
        account_data_with_account_type = self.account_data.copy()
        account_data_with_account_type["account_type"] = long_account_type

        with self.assertRaises(DataError):
            Account.objects.create(**account_data_with_account_type)

    # choice 옵션은 데이터베이스에 반영될 때는 제한 x -> serializer에서 검증
    # 시리얼 라이저가 있는데 어느 정도 레벨에서 까지 검증을 해야할까?
    # def test_bank_code_choices_validation(self) -> None:
    #     invalid_bank_code = "999"
    #     account_data_with_invalid_bank_code = self.account_data.copy()
    #     account_data_with_invalid_bank_code["bank_code"] = invalid_bank_code
    #
    #     try:
    #         Account.objects.create(**account_data_with_invalid_bank_code)
    #         print("성공")
    #     except Exception as e:
    #         print(e)

    # Charfield는 default로 required required field에 대해서 꼭 검증이 필요한가...?
