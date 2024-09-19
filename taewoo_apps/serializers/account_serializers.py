from django.db.models import QuerySet
from rest_framework import serializers

from accounts.models import Account
from taewoo_apps.serializers.user_serializers import UserSerializer


class AccountSerializer(serializers.ModelSerializer[Account]):

    class Meta:
        model = Account
        fields = ["id", "account_type", "balance"]


class AccountCreateSerializer(serializers.ModelSerializer[Account]):

    class Meta:
        model = Account
        fields = ["bank_code", "account_type"]


class AccountListSerializer(serializers.ModelSerializer[Account]):
    user = UserSerializer()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ["user", "account_number", "balance"]

    @staticmethod
    def get_optimized_queryset() -> QuerySet[Account]:
        return Account.objects.select_related("user").only("user", "account_number", "balance")

    def get_balance(self, instance) -> str:  # type: ignore
        return f"{int(instance.balance)}원"


class AccountRetrieveSerializer(serializers.ModelSerializer[Account]):
    user = UserSerializer()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ["user", "account_number", "balance"]

    @staticmethod
    def get_optimized_queryset() -> QuerySet[Account]:
        return Account.objects.select_related("user").only("user", "account_number", "balance")

    def get_balance(self, instance) -> str:  # type: ignore
        return f"{int(instance.balance)}원"


class AccountDestroySerializer(serializers.ModelSerializer[Account]):
    @staticmethod
    def get_optimized_queryset() -> QuerySet[Account]:
        return Account.objects.all()
