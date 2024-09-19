import os

from .base import *

DEBUG = False

ALLOWED_HOSTS = ["3.38.117.147"]

INSTALLED_APPS += [
    "storages",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME", "postgres"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": "5432",
    }
}

# S3 Storage
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.getenv("S3_KEY"),
            "secret_key": os.getenv("S3_SECRET"),
            "bucket_name": os.getenv("S3_NAME"),
            "region_name": os.getenv("S3_REGION"),
            "location": "media",
            "default_acl": "public-read",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.getenv("S3_KEY"),
            "secret_key": os.getenv("S3_SECRET"),
            "bucket_name": os.getenv("S3_NAME"),
            "region_name": os.getenv("S3_REGION"),
            "custom_domain": f'{os.getenv("S3_NAME")}.s3.amazonaws.com',
            "location": "static",
            "default_acl": "public-read",
        },
    },
}

# Static, Media URL
STATIC_URL = f'https://{os.getenv("S3_NAME")}.s3.amazonaws.com/static/'
MEDIA_URL = f'https://{os.getenv("S3_NAME")}.s3.amazonaws.com/media/'
