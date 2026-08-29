from django.db.models import Sum

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import Category, Course
from lessons.models import Lesson, LessonProgress
from enrollments.models import Enrollment


# ==========================================================
# Category Serializer
# ==========================================================

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


# ==========================================================
# Course List Serializer
# ==========================================================

class CourseListSerializer(serializers.ModelSerializer):

    category = CategorySerializer(
        read_only=True
    )

    instructor = serializers.StringRelatedField()

    class Meta:
        model = Course

        fields = (
            "id",
            "title",
            "slug",
            "short_description",
            "thumbnail",
            "level",
            "price",
            "is_free",
            "category",
            "instructor",
        )


# ==========================================================
# Course Detail Serializer
# ==========================================================

class CourseDetailSerializer(serializers.ModelSerializer):

    category = CategorySerializer(
        read_only=True
    )

    instructor = serializers.StringRelatedField()

    total_sections = serializers.SerializerMethodField()
    total_lessons = serializers.SerializerMethodField()
    total_students = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()

    enrolled = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Course

        fields = (
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "thumbnail",
            "level",
            "price",
            "is_free",
            "category",
            "instructor",

            "total_sections",
            "total_lessons",
            "total_students",
            "total_duration",

            "enrolled",
            "progress",
        )

    # ------------------------------------------------------
    # Total Sections
    # ------------------------------------------------------

    @extend_schema_field(serializers.IntegerField)
    def get_total_sections(self, obj) -> int:

        return obj.sections.count()

    # ------------------------------------------------------
    # Total Lessons
    # ------------------------------------------------------

    @extend_schema_field(serializers.IntegerField)
    def get_total_lessons(self, obj) -> int:

        return Lesson.objects.filter(
            section__course=obj,
            is_published=True,
        ).count()

    # ------------------------------------------------------
    # Total Students
    # ------------------------------------------------------

    @extend_schema_field(serializers.IntegerField)
    def get_total_students(self, obj) -> int:

        return obj.enrollments.count()

    # ------------------------------------------------------
    # Total Duration
    # ------------------------------------------------------

    @extend_schema_field(serializers.IntegerField)
    def get_total_duration(self, obj) -> int:

        duration = Lesson.objects.filter(
            section__course=obj,
            is_published=True,
        ).aggregate(
            total=Sum("duration")
        )

        return duration["total"] or 0

    # ------------------------------------------------------
    # Enrollment Status
    # ------------------------------------------------------

    @extend_schema_field(serializers.BooleanField)
    def get_enrolled(self, obj) -> bool:

        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return False

        return Enrollment.objects.filter(
            user=request.user,
            course=obj,
            is_active=True,
        ).exists()

    # ------------------------------------------------------
    # Course Progress
    # ------------------------------------------------------

    @extend_schema_field(serializers.IntegerField)
    def get_progress(self, obj) -> int:

        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return 0

        total_lessons = Lesson.objects.filter(
            section__course=obj,
            is_published=True,
        ).count()

        if total_lessons == 0:
            return 0

        completed = LessonProgress.objects.filter(
            user=request.user,
            lesson__section__course=obj,
            completed=True,
        ).count()

        return int(
            (completed / total_lessons) * 100
        )