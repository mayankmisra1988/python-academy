from rest_framework import generics
from certificates.utils import generate_certificate_pdf
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from enrollments.models import Enrollment
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from certificates.models import Certificate

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



def update_course_completion(user, course):
    """
    Update enrollment completion based on lesson progress.
    """

    total_lessons = Lesson.objects.filter(
        section__course=course,
        is_published=True,
    ).count()

    completed_lessons = LessonProgress.objects.filter(
        user=user,
        completed=True,
        lesson__section__course=course,
    ).count()

    enrollment = Enrollment.objects.filter(
        user=user,
        course=course,
    ).first()

    if enrollment is None:
        return

    if (
        total_lessons > 0
        and completed_lessons == total_lessons
    ):
        enrollment.completed = True
        enrollment.completed_at = timezone.now()

    else:
        enrollment.completed = False
        enrollment.completed_at = None

    enrollment.save(
        update_fields=[
            "completed",
            "completed_at",
        ]
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


class LessonProgressDetailView(
    generics.RetrieveUpdateAPIView
):

    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return LessonProgress.objects.filter(
            user=self.request.user
        )

    def perform_update(self, serializer):

        progress = serializer.save()

        update_course_completion(
            self.request.user,
            progress.lesson.section.course,
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

        # ==================================================
        # CREATE QUIZ ATTEMPT
        # ==================================================

        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
        )

        total_questions = quiz.questions.count()
        correct_answers = 0

        # ==================================================
        # CHECK ANSWERS
        # ==================================================

        for item in serializer.validated_data["answers"]:

            try:

                question = quiz.questions.get(
                    id=item["question"]
                )

            except Question.DoesNotExist:

                continue

            try:

                option = question.options.get(
                    id=item["option"]
                )

            except Option.DoesNotExist:

                continue

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

                if (
                    created
                    or not certificate.pdf
                ):

                    generate_certificate_pdf(
                        certificate
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