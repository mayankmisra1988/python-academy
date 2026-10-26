from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from enrollments.models import Enrollment

from .models import (
    Section,
    Lesson,
    LessonProgress,
    Quiz,
    Question,
    Option,
    QuizAttempt,
    StudentAnswer,
)


# ==========================================================
# Option Serializer
# ==========================================================

class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            "id",
            "option_text",
        )


# ==========================================================
# Question Serializer
# ==========================================================

class QuestionSerializer(serializers.ModelSerializer):

    options = OptionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Question
        fields = (
            "id",
            "question",
            "order",
            "marks",
            "options",
        )


# ==========================================================
# Quiz Serializer
# ==========================================================

class QuizSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Quiz
        fields = (
            "id",
            "title",
            "description",
            "passing_score",
            "time_limit",
            "questions",
            "is_active",
            "lesson",
        )


# ==========================================================
# Lesson Serializer
# ==========================================================

class LessonSerializer(serializers.ModelSerializer):

    quiz = QuizSerializer(
        read_only=True,
    )

    course_id = serializers.IntegerField(
        source="section.course.id",
        read_only=True,
    )

    section_id = serializers.IntegerField(
        source="section.id",
        read_only=True,
    )

    section_title = serializers.CharField(
        source="section.title",
        read_only=True,
    )

    course_slug = serializers.CharField(
        source="section.course.slug",
        read_only=True,
    )

    notes_url = serializers.SerializerMethodField()

    has_quiz = serializers.SerializerMethodField()

    completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson

        fields = (
            "id",
            "title",
            "description",
            "video_url",
            "notes",
            "duration",
            "is_preview",
            "is_published",
            "order",
            "course_id",
            "section_id",
            "section_title",
            "course_slug",
            "notes_url",
            "quiz",
            "has_quiz",
            "completed",
        )

    @extend_schema_field(serializers.URLField(allow_null=True))
    def get_notes_url(self, obj) -> str | None:

        request = self.context.get("request")

        if obj.notes:

            if request:
                return request.build_absolute_uri(
                    obj.notes.url
                )

            return obj.notes.url

        return None

    @extend_schema_field(serializers.BooleanField)
    def get_has_quiz(self, obj) -> bool:

        return hasattr(obj, "quiz")

    @extend_schema_field(serializers.BooleanField)
    def get_completed(self, obj) -> bool:

        request = self.context.get("request")

        if not request or request.user.is_anonymous:
            return False

        return LessonProgress.objects.filter(
            user=request.user,
            lesson=obj,
            completed=True,
        ).exists()


# ==========================================================
# Section Serializer
# ==========================================================

class SectionSerializer(serializers.ModelSerializer):

    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Section

        fields = (
            "id",
            "title",
            "description",
            "order",
            "lessons",
        )

    def get_lessons(self, obj):
        request = self.context.get("request")
        course = obj.course

        has_active_enrollment = False

        if request and request.user.is_authenticated:
            if not course.is_free:
                has_active_enrollment = Enrollment.objects.filter(
                    user=request.user,
                    course=course,
                    is_active=True,
                ).exists()

        published_lessons = obj.lessons.filter(
            is_published=True
        ).order_by("order")

        results = []

        for lesson in published_lessons:
            can_access_content = (
                course.is_free
                or lesson.is_preview
                or has_active_enrollment
            )

            if can_access_content:
                results.append(
                    LessonSerializer(
                        lesson,
                        context=self.context,
                    ).data
                )
            else:
                # Locked lessons: return curriculum metadata only.
                results.append({
                    "id": lesson.id,
                    "title": lesson.title,
                    "description": lesson.description,
                    "duration": lesson.duration,
                    "is_preview": lesson.is_preview,
                    "is_published": lesson.is_published,
                    "order": lesson.order,
                    "course_id": course.id,
                    "section_id": obj.id,
                    "section_title": obj.title,
                    "course_slug": course.slug,
                    "video_url": None,
                    "notes": None,
                    "notes_url": None,
                    "quiz": None,
                    "has_quiz": False,
                    "completed": False,
                })

        return results



# ==========================================================
# Lesson Progress Serializer
# ==========================================================

class LessonProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonProgress

        fields = (
            "id",
            "lesson",
            "completed",
            "watched_percentage",
            "last_watched_at",
        )

        read_only_fields = (
            "id",
            "last_watched_at",
        )

    def validate_watched_percentage(self, value):

        if value < 0 or value > 100:

            raise serializers.ValidationError(
                "Watched percentage must be between 0 and 100."
            )

        return value

    def validate(self, attrs):

        completed = attrs.get(
            "completed",
            False,
        )

        watched = attrs.get(
            "watched_percentage",
            0,
        )

        if completed and watched < 100:

            raise serializers.ValidationError(
                {
                    "watched_percentage":
                    "Completed lesson must have 100% watched."
                }
            )

        return attrs


# ==========================================================
# Quiz Submit Serializer
# ==========================================================

class StudentAnswerInputSerializer(serializers.Serializer):

    question = serializers.IntegerField()

    option = serializers.IntegerField()


class QuizSubmitSerializer(serializers.Serializer):

    answers = StudentAnswerInputSerializer(
        many=True
    )


# ==========================================================
# Student Answer Serializer
# ==========================================================

class StudentAnswerSerializer(serializers.ModelSerializer):

    question = QuestionSerializer(
        read_only=True,
    )

    selected_option = OptionSerializer(
        read_only=True,
    )

    class Meta:
        model = StudentAnswer

        fields = (
            "question",
            "selected_option",
            "is_correct",
        )


# ==========================================================
# Quiz Attempt Serializer
# ==========================================================

class QuizAttemptSerializer(serializers.ModelSerializer):

    answers = StudentAnswerSerializer(
        many=True,
        read_only=True,
    )

    course_id = serializers.SerializerMethodField()

    class Meta:
        model = QuizAttempt

        fields = (
            "id",
            "course_id",
            "student",
            "quiz",
            "total_questions",
            "correct_answers",
            "score",
            "passed",
            "started_at",
            "submitted_at",
            "answers",
            "percentage",
        )

    @extend_schema_field(serializers.IntegerField)
    def get_course_id(self, obj) -> int:

        return obj.quiz.lesson.section.course.id