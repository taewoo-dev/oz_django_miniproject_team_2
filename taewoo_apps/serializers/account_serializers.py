from typing import Any

from django.db.models import QuerySet
from rest_framework import serializers

from accounts.models import Account
from taewoo_apps.serializers.user_serializers import UserSerializer


class AccountCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ["bank_code", "account_type"]


class AccountListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ["user", "account_number", "balance"]

    @staticmethod
    def get_optimized_queryset() -> QuerySet[Account]:
        return Account.objects.select_related("user").only("user", "account_number", "balance")

    def get_balance(self, instance) -> str:
        return f"{int(instance.balance)}원"


class AccountRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    balance = serializers.SerializerMethodField()
    # transaction_history 필드 추가

    class Meta:
        model = Account
        fields = ["user", "account_number", "balance"]

    @staticmethod
    def get_optimized_queryset() -> QuerySet[Account]:
        return Account.objects.select_related("user").only("user", "account_number", "balance")

    def get_balance(self, instance) -> str:
        return f"{int(instance.balance)}원"


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["user", "account_number", "balance"]
