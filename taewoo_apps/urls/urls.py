from django.urls import include, path

urlpatterns = []

urlpatterns_api_v1 = [
    path("auth/", include("taewoo_apps.urls.auth_urls")),  # auth
    path("oauth/", include("taewoo_apps.urls.oauth_urls")),  # oauth
]

urlpatterns += [
    path("api/", include((urlpatterns_api_v1, "api-v1"))),
]
