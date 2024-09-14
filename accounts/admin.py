from django.contrib import admin

from accounts.models import Account


# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ("user", "account_number", "bank_code", "account_type", "balance")
