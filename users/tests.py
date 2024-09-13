import uuid

from django.test import TestCase

from .models import User


class UserModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="testuser@example.com",
            nickname="testnickname",
            name="testuser",
            phone_number="1234567890",
            password="password",
        )

    def test_user_creation(self) -> None:
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.nickname, "testnickname")
        self.assertTrue(self.user.check_password("password"))

    def test_user_str_method(self) -> None:
        self.assertEqual(str(self.user), f"{self.user.email}")


# class AccountModelTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='testuser@example.com',
#             nickname='testnickname',
#             name='testuser',
#             phone_number='1234567890',
#             password='testpassword',
#         )
#         self.account = Account.objects.create(
#             user_id=self.user,
#             account_number='1234567890',
#             bank_code='KB',
#             account_type='SAVINGS',
#             balance=100000
#         )
#
#     def test_account_creation(self):
#         self.assertEqual(self.account.user_id, self.user)
#         self.assertEqual(self.account.account_number, '1234567890')
#         self.assertEqual(self.account.balance, 100000)
#
#     def test_account_str_method(self):
#         self.assertEqual(str(self.account),  f"{self.account_id} - {self.transaction_type} - {self.transaction_amount}")
#
# class TransactionModelTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='testuser@example.com',
#             nickname='testnickname',
#             name='testuser',
#             phone_number='01012345678',
#             password='testpassword'
#         )
#         self.account = Account.objects.create(
#             user_id=self.user,
#             account_number='1234567890',
#             bank_code='KB',
#             account_type='SAVINGS',
#             balance=10000
#         )
#         self.transaction = Transaction_history.objects.create(
#             account_id=self.account,
#             transaction_amount=5000,
#             transaction_balance=5000,
#             transaction_description="Test deposit",
#             transaction_type='DEPOSIT',
#             payment_method='CASH'
#         )
#
#     def test_transaction_creation(self):
#         self.assertEqual(self.transaction.account_id, self.account)
#         self.assertEqual(self.transaction.transaction_amount, 5000)
#         self.assertEqual(self.transaction.transaction_balance, 5000)
#         self.assertEqual(self.transaction.transaction_description, "Test deposit")
#
#     def test_transaction_str_method(self):
#         self.assertEqual(str(self.transaction), f"{self.account_id} - {self.transaction_type} - {self.transaction_amount}")
