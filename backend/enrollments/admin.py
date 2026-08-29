from django.contrib import admin

from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display=(
        "user",
        "course",
        "is_active",
        "completed",
        "enrolled_at",
    )

    list_filter=(
        "is_active",
        "completed",
    )

    search_fields=(
        "user__username",
        "course__title",
    )
    readonly_fields=(
        "enrolled_at",
        "completed_at",
    )

    list_select_related=(
        "user",
        "course",
    )