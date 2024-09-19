from django.urls import include, path

from accounts.views import (
    AccountCreateAPIView,
    AccountDestroyAPIView,
    AccountListAPIView,
    AccountRetrieveAPIView,
)

urlpatterns = [
    path("new/", AccountCreateAPIView.as_view(), name="account_new"),
    path("", AccountListAPIView.as_view(), name="account_list"),
    path("<int:pk>/", AccountRetrieveAPIView.as_view(), name="account_detail"),
    path("<int:pk>/delete/", AccountDestroyAPIView.as_view(), name="account_delete"),
]
