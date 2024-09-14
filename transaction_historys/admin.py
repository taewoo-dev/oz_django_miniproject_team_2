from django.contrib import admin

from transaction_historys.models import TransactionHistory

# Register your models here.


@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ("account", "transaction_amount", "transaction_balance", "transaction_type")
