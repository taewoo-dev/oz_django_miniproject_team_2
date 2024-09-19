from django.urls import path, include

from taewoo_apps.views.transaction_history_views import (
    TransactionHistoryCreateAPIView,
    TransactionHistoryListAPIView,
    TransactionHistoryRetrieveAPIView,
)

urlpatterns = []

urlpatterns_api_v1 = [
    # account url
    path("new/", TransactionHistoryCreateAPIView.as_view(), name="transaction_new"),
    path("", TransactionHistoryListAPIView.as_view(), name="transaction_list"),
    path("<int:pk>/", TransactionHistoryRetrieveAPIView.as_view(), name="transaction_detail"),
]


urlpatterns += [
    path("", include((urlpatterns_api_v1, "api-transaction-v1"))),
]
