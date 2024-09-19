from django.db.models import QuerySet
from rest_framework import serializers

from taewoo_apps.serializers.account_serializers import AccountSerializer
from transaction_historys.models import TransactionHistory


class TransactionHistoryCreateSerializer(serializers.ModelSerializer[TransactionHistory]):

    class Meta:
        model = TransactionHistory
        fields = [
            "account",
            "transaction_amount",
            "transaction_balance",
            "transaction_type",
            "payment_method",
            "transaction_description",
        ]


class TransactionHistorySerializer(serializers.ModelSerializer[TransactionHistory]):
    account = AccountSerializer()


    class Meta:
        model = TransactionHistory
        fields = [
            "account",
            "transaction_amount",
            "transaction_balance",
            "transaction_type",
            "payment_method",
            "transaction_description",
        ]

    @staticmethod
    def get_optimized_queryset() -> QuerySet[TransactionHistory]:
        return TransactionHistory.objects.all()
