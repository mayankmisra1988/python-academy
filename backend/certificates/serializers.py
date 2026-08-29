from rest_framework import serializers

from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):

    course_title = serializers.CharField(
        source="course.title",
        read_only=True,
    )

    course_slug = serializers.CharField(
        source="course.slug",
        read_only=True,
    )

    thumbnail = serializers.ImageField(
        source="course.thumbnail",
        read_only=True,
    )

    class Meta:
        model = Certificate
        fields = (
            "id",
            "certificate_id",
            "course",
            "course_title",
            "course_slug",
            "thumbnail",
            "pdf",
            "issued_at",
        )

        read_only_fields = (
            "certificate_id",
            "pdf",
            "issued_at",
        )