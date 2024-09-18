from django.urls import path, include

from taewoo_apps.views.account_views import (
    AccountCreateAPIView,
    AccountListAPIView,
    AccountRetrieveAPIView,
    AccountUpdateAPIView,
    AccountDestroyAPIView,
)

urlpatterns = []

urlpatterns_api_v1 = [
    # account url
    path("new/", AccountCreateAPIView.as_view(), name="account_new"),
    path("", AccountListAPIView.as_view(), name="account_list"),
    path("<int:pk>/", AccountRetrieveAPIView.as_view(), name="account_detail"),
    path("<int:pk>/edit/", AccountUpdateAPIView.as_view(), name="account_edit"),
    path("<int:pk>/delete/", AccountDestroyAPIView.as_view(), name="account_delete"),
]


urlpatterns += [
    path("", include((urlpatterns_api_v1, "api-account-v1"))),
]
