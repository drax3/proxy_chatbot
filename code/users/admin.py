from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "full_name", "is_staff", "is_active", "mobile")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password", "full_name", "mobile")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name","mobile", "password1", "password2", "is_staff", "is_active")}
         ),
    )
