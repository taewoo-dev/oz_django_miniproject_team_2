# Generated by Django 5.1.1 on 2024-09-18 18:41


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_user_nickname_alter_user_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(
                default=False,
                help_text="사용자가 활성상태로 처리될 지 여부를 지정합니다.(사용자를 삭제하지 않고 비활성화하려면 선택해제)",
                verbose_name="active",
            ),
        ),
    ]
