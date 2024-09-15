from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_verification_email(user, verification_url):  # type: ignore
    email_title: str = "이메일 인증해 주세요."
    email_body: str = render_to_string(
        "users/email_verification.html", {"verification_url": verification_url, "user": user}
    )
    send_mail(
        email_title,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
