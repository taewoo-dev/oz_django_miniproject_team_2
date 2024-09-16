# Generated by Django 5.1.1 on 2024-09-15 16:24

import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_created_at_user_updated_at_alter_user_nickname"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="nickname",
            field=models.CharField(
                blank=True,
                error_messages={"unique": "이미 nickname이 존재합니다."},
                help_text="문자, 숫자, 특수문자( @/./+/-/_ )를 이용해 닉네임을 만들어주세요.",
                max_length=100,
                null=True,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name="nickname",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(
                blank=True,
                max_length=20,
                null=True,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="핸드폰번호는 010-xxxx-xxxx 형식으로 만들어주세요.", regex="010-\\d{4}-\\d{4}$"
                    )
                ],
            ),
        ),
    ]
