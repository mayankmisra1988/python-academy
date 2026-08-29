from django.contrib import admin

from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):

    list_display = (
        "certificate_id",
        "user",
        "course",
        "issued_at",
    )

    list_filter = (
        "issued_at",
    )

    search_fields = (
        "certificate_id",
        "user__email",
        "course__title",
    )

    readonly_fields = (
        "certificate_id",
        "issued_at",
    )

    ordering = (
        "-issued_at",
    )
