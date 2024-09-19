from django.urls import include, path

from taewoo_apps.views.account_views import (
    AccountCreateAPIView,
    AccountDestroyAPIView,
    AccountListAPIView,
    AccountRetrieveAPIView,
)

urlpatterns = []

urlpatterns_api_v1 = [
    # accounts urls
    path("new/", AccountCreateAPIView.as_view(), name="account_new"),
    path("", AccountListAPIView.as_view(), name="account_list"),
    path("<int:pk>/", AccountRetrieveAPIView.as_view(), name="account_detail"),
    path("<int:pk>/delete/", AccountDestroyAPIView.as_view(), name="account_delete"),
]


urlpatterns += [
    path("", include((urlpatterns_api_v1, "api-account-v1"))),
]
