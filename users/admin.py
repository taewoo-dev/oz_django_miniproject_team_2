from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ("nickname", "name", "phone_number", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("nickname", "name", "email", "phone_number")}),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
