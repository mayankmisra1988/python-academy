from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import Enrollment
from lessons.models import Lesson


# ==========================================================
# Enrollment Serializer
# ==========================================================

class EnrollmentSerializer(serializers.ModelSerializer):

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

    progress = serializers.SerializerMethodField()

    lesson_id = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment

        fields = (
            "id",
            "course",
            "course_title",
            "course_slug",
            "thumbnail",
            "lesson_id",
            "enrolled_at",
            "is_active",
            "completed",
            "completed_at",
            "progress",
        )

        read_only_fields = (
            "enrolled_at",
            "completed_at",
        )

    # ------------------------------------------------------
    # Course Progress
    # ------------------------------------------------------

    @extend_schema_field(serializers.IntegerField)
    def get_progress(self, obj) -> int:

        total = obj.course.sections.values_list(
            "lessons",
            flat=True,
        ).count()

        if total == 0:
            return 0

        completed = obj.user.lesson_progress.filter(
            lesson__section__course=obj.course,
            completed=True,
        ).count()

        return int(
            (completed / total) * 100
        )

    # ------------------------------------------------------
    # First Lesson ID
    # ------------------------------------------------------

    @extend_schema_field(
        serializers.IntegerField(allow_null=True)
    )
    def get_lesson_id(self, obj) -> int | None:

        first_lesson = (
            Lesson.objects.filter(
                section__course=obj.course,
                is_published=True,
            )
            .order_by(
                "section__order",
                "order",
            )
            .first()
        )

        if first_lesson:
            return first_lesson.id

        return None

    # ------------------------------------------------------
    # Course Validation
    # ------------------------------------------------------

    def validate_course(self, value):

        request = self.context["request"]

        if not value.is_published:

            raise serializers.ValidationError(
                "This course is not available."
            )

        if Enrollment.objects.filter(
            user=request.user,
            course=value,
        ).exists():

            raise serializers.ValidationError(
                "You are already enrolled in this course."
            )

        return value