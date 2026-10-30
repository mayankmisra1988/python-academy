
import logging
from django.db import transaction
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from certificates.models import Certificate
from certificates.utils import generate_certificate_pdf
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

from .serializers import (
    SectionSerializer,
    LessonSerializer,
    LessonProgressSerializer,
    QuizSerializer,
    QuizSubmitSerializer,
    QuizAttemptSerializer,
)
logger = logging.getLogger(__name__)


class CourseCurriculumView(generics.ListAPIView):

    serializer_class = SectionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Section.objects.filter(
                course_id=self.kwargs["course_id"]
            )
            .prefetch_related("lessons")
            .order_by("order")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class LessonDetailView(generics.RetrieveAPIView):
    """
    Returns published lessons only when access is permitted.
    Preview lessons and free-course lessons are public.
    Paid-course lessons require an active enrollment,
    unless the lesson is marked as preview.
    """

    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Lesson.objects.filter(
            is_published=True
        ).select_related(
            "section",
            "section__course",
        )

    def get_object(self):
        from django.http import Http404

        lesson = super().get_object()
        course = lesson.section.course

        if lesson.is_preview or course.is_free:
            return lesson

        if not self.request.user.is_authenticated:
            raise Http404

        has_enrollment = Enrollment.objects.filter(
            user=self.request.user,
            course=course,
            is_active=True,
        ).exists()

        if not has_enrollment:
            raise Http404

        return lesson

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context



def lesson_quiz_passed(user, lesson):
    try:
        quiz = lesson.quiz
    except Quiz.DoesNotExist:
        return True

    # Inactive quiz is not a completion requirement.
    if not quiz.is_active:
        return True

    return QuizAttempt.objects.filter(
        student=user,
        quiz=quiz,
        passed=True,
    ).exists()


def update_course_completion(user, course):
    lessons = list(
        Lesson.objects.filter(
            section__course=course,
            is_published=True,
        ).select_related("quiz")
    )

    enrollment = Enrollment.objects.filter(
        user=user,
        course=course,
        is_active=True,
    ).first()

    if enrollment is None:
        return

    completed_lesson_ids = set(
        LessonProgress.objects.filter(
            user=user,
            completed=True,
            lesson__in=lessons,
        ).values_list("lesson_id", flat=True)
    )

    all_lessons_completed = (
        bool(lessons)
        and len(completed_lesson_ids) == len(lessons)
    )

    all_quizzes_passed = all(
        lesson_quiz_passed(user, lesson)
        for lesson in lessons
    )

    course_completed = (
        all_lessons_completed
        and all_quizzes_passed
    )

    was_completed = enrollment.completed

    enrollment.completed = course_completed

    if course_completed and not was_completed:
        enrollment.completed_at = timezone.now()
    elif not course_completed:
        enrollment.completed_at = None

    enrollment.save(
        update_fields=["completed", "completed_at"]
    )

def require_course_access(user, course):
    """
    Free courses are accessible.
    Paid courses require an active enrollment.
    """
    if course.is_free:
        return

    has_active_enrollment = Enrollment.objects.filter(
        user=user,
        course=course,
        is_active=True,
    ).exists()

    if not has_active_enrollment:
        raise PermissionDenied(
            "Active enrollment is required to access this paid course."
        )



class LessonProgressView(generics.ListCreateAPIView):

    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return (
            LessonProgress.objects.filter(
                user=self.request.user
            )
            .select_related(
                "lesson",
                "lesson__section",
                "lesson__section__course",
            )
        )

    def perform_create(self, serializer):

        lesson = serializer.validated_data["lesson"]
        if not lesson.is_published:
            raise PermissionDenied(
                "This lesson is not available."
            )

        require_course_access(
            self.request.user,
            lesson.section.course,
        )
        if serializer.validated_data.get("completed", False):
            lesson = serializer.validated_data["lesson"]

            if not lesson_quiz_passed(self.request.user, lesson):
                raise ValidationError(
                    "You must pass this lesson's quiz before completing it."
                )

        progress, created = (
            LessonProgress.objects.update_or_create(
                user=self.request.user,
                lesson=lesson,
                defaults={
                    "completed": serializer.validated_data.get(
                        "completed",
                        False,
                    ),
                    "watched_percentage": serializer.validated_data.get(
                        "watched_percentage",
                        0,
                    ),
                },
            )
        )

        # DRF response ke liye instance set karo
        serializer.instance = progress

        update_course_completion(
            self.request.user,
            lesson.section.course,
        )


class LessonProgressDetailView(generics.RetrieveUpdateAPIView):

    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return LessonProgress.objects.filter(
            user=self.request.user
        )

    def perform_update(self, serializer):
        existing_lesson = serializer.instance.lesson
        new_lesson = serializer.validated_data.get(
            "lesson",
            existing_lesson,
        )

        # Existing aur target lesson dono ka access verify karo.
        for lesson in {existing_lesson, new_lesson}:
            if not lesson.is_published:
                raise PermissionDenied(
                    "This lesson is not available."
                )

            require_course_access(
                self.request.user,
                lesson.section.course,
            )

        completed = serializer.validated_data.get(
            "completed",
            serializer.instance.completed,
        )

        if completed and not lesson_quiz_passed(
            self.request.user,
            new_lesson,
        ):
            raise ValidationError(
                "You must pass this lesson's quiz before completing it."
            )

        progress = serializer.save()

        old_course = existing_lesson.section.course
        new_course = progress.lesson.section.course

        update_course_completion(
            self.request.user,
            old_course,
        )

        if new_course.pk != old_course.pk:
            update_course_completion(
                self.request.user,
                new_course,
            )


class QuizDetailView(generics.GenericAPIView):
    """
    Return quiz of a lesson.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer

    def get(self, request, lesson_id):

        try:

            quiz = (
                Quiz.objects.prefetch_related(
                    "questions__options"
                )
                .get(
                    lesson_id=lesson_id,
                    is_active=True,
                )
            )

        except Quiz.DoesNotExist:

            return Response(
                {
                    "detail": "Quiz not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if not quiz.lesson.is_published:
            raise PermissionDenied(
                "This lesson is not available."
            )

        require_course_access(
            request.user,
            quiz.lesson.section.course,
        )

        serializer = self.get_serializer(quiz)

        return Response(serializer.data)


class QuizSubmitView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = QuizSubmitSerializer

    @transaction.atomic
    def post(self, request, quiz_id):

        # ==================================================
        # VALIDATE ANSWERS
        # ==================================================

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        # ==================================================
        # GET QUIZ
        # ==================================================

        try:

            quiz = (
                Quiz.objects
                .prefetch_related(
                    "questions__options"
                )
                .select_related(
                    "lesson",
                    "lesson__section",
                    "lesson__section__course",
                )
                .get(
                    id=quiz_id,
                    is_active=True,
                )
            )

        except Quiz.DoesNotExist:

            return Response(
                {
                    "detail": "Quiz not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if not quiz.lesson.is_published:
            raise PermissionDenied(
                "This lesson is not available."
            )

        require_course_access(
            request.user,
            quiz.lesson.section.course,
        )
        questions = {
            question.id: question
            for question in quiz.questions.all()
        }

        if not questions:
            raise ValidationError({
                "quiz": "This quiz has no questions and cannot be submitted."
            })

        validated_answers = []

        for item in serializer.validated_data["answers"]:
            question = questions.get(item["question"])

            if question is None:
                raise ValidationError({
                    "answers": (
                        "A submitted question does not belong to this quiz."
                    )
                })
            option = next(
                (
                    option
                    for option in question.options.all()
                    if option.id == item["option"]
                ),
                None,
            )
            if option is None:
                raise ValidationError({
                    "answers": (
                        "A selected option does not belong to its question."
                    )
                })

            validated_answers.append((question, option))

        # CREATE QUIZ ATTEMPT
        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
        )

        total_questions = len(questions)
        correct_answers = 0

        # CHECK ANSWERS
        for question, option in validated_answers:
            is_correct = option.is_correct

            if is_correct:
                correct_answers += 1

            StudentAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_option=option,
                is_correct=is_correct,
            )

        # ==================================================
        # CALCULATE RESULT
        # ==================================================

        percentage = 0

        if total_questions > 0:

            percentage = round(
                (
                    correct_answers
                    / total_questions
                ) * 100,
                2,
            )

        passed = (
            percentage >= quiz.passing_score
        )

        # ==================================================
        # SAVE ATTEMPT
        # ==================================================

        attempt.total_questions = total_questions
        attempt.correct_answers = correct_answers
        attempt.percentage = percentage
        attempt.score = percentage
        attempt.passed = passed

        attempt.save()

        # ==================================================
        # DEFAULT CERTIFICATE
        # ==================================================

        certificate = None

        # ==================================================
        # IF QUIZ PASSED
        # ==================================================

        if passed:

            current_lesson = quiz.lesson
            course = current_lesson.section.course

            # ==================================================
            # MARK CURRENT LESSON COMPLETED
            # ==================================================

            LessonProgress.objects.update_or_create(

                user=request.user,

                lesson=current_lesson,

                defaults={
                    "watched_percentage": 100,
                    "completed": True,
                },
            )

            # ==================================================
            # UPDATE COURSE COMPLETION
            # ==================================================

            update_course_completion(
                request.user,
                course,
            )

            # ==================================================
            # GET ENROLLMENT
            # ==================================================

            enrollment = Enrollment.objects.filter(
                user=request.user,
                course=course,
                is_active=True,
            ).first()

            # ==================================================
            # COURSE COMPLETED
            # ==================================================

            if enrollment and enrollment.completed:

                # ==================================================
                # CREATE / GET CERTIFICATE
                # ==================================================

                certificate, created = (
                    Certificate.objects.get_or_create(
                        user=request.user,
                        course=course,
                    )
                )

                # ==================================================
                # GENERATE PDF
                # ==================================================

                if created or not certificate.pdf:
                    try:
                        generate_certificate_pdf(certificate)
                    except Exception:
                        logger.exception(
                            "Certificate PDF generation failed for certificate_id=%s",
                            certificate.certificate_id,
                        )
        # ==================================================
        # SERIALIZE RESULT
        # ==================================================

        response_data = QuizAttemptSerializer(
            attempt
        ).data

        # ==================================================
        # ADD CERTIFICATE
        # ==================================================

        if certificate:

            response_data["certificate"] = {

                "id": certificate.id,

                "certificate_id":
                    certificate.certificate_id,

                "pdf":
                    certificate.pdf.url
                    if certificate.pdf
                    else None,

                "issued_at":
                    certificate.issued_at,

            }

        else:

            response_data["certificate"] = None

        # ==================================================
        # RESPONSE
        # ==================================================

        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
        )