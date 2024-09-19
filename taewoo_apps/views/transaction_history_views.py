from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from taewoo_apps.serializers.transaction_history_serializers import (
    TransactionHistoryCreateSerializer,
    TransactionHistorySerializer,
)


class TransactionHistoryCreateAPIView(CreateAPIView):  # type: ignore
    serializer_class = TransactionHistoryCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer) -> None:  # type: ignore
        account = serializer.validated_data["account"]
        transaction_amount = serializer.validated_data["transaction_amount"]
        transaction_type = serializer.validated_data["transaction_type"]
        transaction_after_amount = serializer.validated_data["transaction_after_balance"]
        transaction_balance = 0

        # 출금일 경우
        if transaction_type == "withdrawal":
            if account.account_type == "deposit" and account.balance < transaction_amount:
                raise ValidationError("계좌 잔액이 부족합니다.")
            transaction_balance = account.balance - transaction_amount

        # 입금일 경우
        if transaction_type == "deposit":
            transaction_balance = account.balance + transaction_amount

        transaction_after_balance = account.balance
        account.balance = transaction_balance

        account.save()

        serializer.save(transaction_balance=transaction_balance)


class TransactionHistoryListAPIView(ListAPIView):  # type: ignore
    queryset = TransactionHistorySerializer.get_optimized_queryset()
    serializer_class = TransactionHistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination


class TransactionHistoryRetrieveAPIView(RetrieveAPIView):  # type: ignore
    queryset = TransactionHistorySerializer.get_optimized_queryset()
    serializer_class = TransactionHistorySerializer
    permission_classes = [IsAuthenticated]
