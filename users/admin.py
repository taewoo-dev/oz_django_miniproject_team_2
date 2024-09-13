# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
#
# from .models import User
#
#
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     list_display = ("nickname", "name", "phone_number", "is_active")
#     fieldsets = (
#         (None, {"fields": ("username", "password")}),
#         (("Personal info"), {"fields": ("nickname", "name", "email", "phone_number")}),
#         (("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )
