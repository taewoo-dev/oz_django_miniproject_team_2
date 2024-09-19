from django.urls import path

from transaction_historys.views import (
    TransactionHistoryCreateAPIView,
    TransactionHistoryListAPIView,
    TransactionHistoryRetrieveAPIView,
)

urlpatterns = [
    path("new/", TransactionHistoryCreateAPIView.as_view(), name="transaction_new"),
    path("", TransactionHistoryListAPIView.as_view(), name="transaction_list"),
    path("<int:pk>/", TransactionHistoryRetrieveAPIView.as_view(), name="transaction_detail"),
]
