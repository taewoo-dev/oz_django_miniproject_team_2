import random

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from taewoo_apps.serializers.account_serializers import (
    AccountCreateSerializer,
    AccountListSerializer,
    AccountRetrieveSerializer,
    AccountDestroySerializer,
)


class AccountCreateAPIView(CreateAPIView):
    serializer_class = AccountCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer) -> None:
        account_number = self._generate_account_number()
        user = self.request.user
        serializer.save(user=user, account_number=account_number)

    def _generate_account_number(self) -> str:
        branch_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        account_type_code = "".join([str(random.randint(0, 9)) for _ in range(2)])
        unique_number = "".join([str(random.randint(0, 9)) for _ in range(6)])

        return f"{branch_code}-{account_type_code}-{unique_number}"


class AccountListAPIView(ListAPIView):
    queryset = AccountListSerializer.get_optimized_queryset()
    serializer_class = AccountListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination


class AccountRetrieveAPIView(RetrieveAPIView):
    queryset = AccountRetrieveSerializer.get_optimized_queryset()
    serializer_class = AccountRetrieveSerializer
    permission_classes = [IsAuthenticated]


class AccountDestroyAPIView(DestroyAPIView):
    queryset = AccountDestroySerializer.get_optimized_queryset()
    permission_classes = [IsAuthenticated]
