from django.db.models import QuerySet
from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ["user", "account_number", "bank_code", "account_type", "balance"]

    @staticmethod
    def get_optimized_queryset() -> QuerySet[Account]:
        return Account.objects.all()
