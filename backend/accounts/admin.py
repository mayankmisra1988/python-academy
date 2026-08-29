from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ("email",)

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "role",
        "is_verified",
        "is_staff",
    )

    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "role",
                    "phone",
                    "bio",
                    "profile_image",
                    "date_of_birth",
                    "is_verified",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "role",
                )
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "learning_streak",
        "completed_courses",
        "total_certificates",
    )