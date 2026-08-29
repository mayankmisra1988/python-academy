from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from enrollments.models import Enrollment
from lessons.models import Lesson, LessonProgress

from .serializers import DashboardSerializer


class DashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DashboardSerializer

    def get(self, request):
        user = request.user

        # =====================================================
        # ACTIVE ENROLLMENTS
        # =====================================================

        enrollments = (
            Enrollment.objects.filter(
                user=user,
                is_active=True,
            )
            .select_related("course")
        )

        total_courses = enrollments.count()

        completed_courses = enrollments.filter(
            completed=True
        ).count()

        in_progress_courses = (
            total_courses - completed_courses
        )

        # =====================================================
        # OVERALL LESSON PROGRESS
        # =====================================================

        course_ids = enrollments.values_list(
            "course_id",
            flat=True,
        )

        total_lessons = Lesson.objects.filter(
            section__course_id__in=course_ids,
            is_published=True,
        ).count()

        completed_lessons = LessonProgress.objects.filter(
            user=user,
            completed=True,
            lesson__section__course_id__in=course_ids,
        ).count()

        overall_progress = 0

        if total_lessons > 0:
            overall_progress = round(
                (completed_lessons / total_lessons) * 100
            )

        # =====================================================
        # CONTINUE LEARNING
        # =====================================================

        continue_learning = []

        for enrollment in enrollments:

            course = enrollment.course

            # -------------------------------------------------
            # ALL PUBLISHED LESSONS
            # -------------------------------------------------

            lessons = list(
                Lesson.objects.filter(
                    section__course=course,
                    is_published=True,
                )
                .order_by(
                    "section__order",
                    "order",
                )
            )

            lessons_count = len(lessons)

            # -------------------------------------------------
            # COMPLETED LESSONS
            # -------------------------------------------------

            completed_lesson_ids = set(
                LessonProgress.objects.filter(
                    user=user,
                    lesson__section__course=course,
                    completed=True,
                ).values_list(
                    "lesson_id",
                    flat=True,
                )
            )

            completed_count = len(
                completed_lesson_ids
            )

            # -------------------------------------------------
            # COURSE PROGRESS
            # -------------------------------------------------

            progress = 0

            if lessons_count > 0:
                progress = round(
                    (
                        completed_count
                        / lessons_count
                    )
                    * 100
                )

            # -------------------------------------------------
            # FIRST INCOMPLETE LESSON
            # -------------------------------------------------

            next_lesson = next(
                (
                    lesson
                    for lesson in lessons
                    if lesson.id
                    not in completed_lesson_ids
                ),
                None,
            )

            # -------------------------------------------------
            # COURSE COMPLETED
            # -------------------------------------------------

            course_completed = (
                lessons_count > 0
                and completed_count >= lessons_count
            )

            # -------------------------------------------------
            # THUMBNAIL
            # -------------------------------------------------

            thumbnail = None

            if course.thumbnail:
                thumbnail = request.build_absolute_uri(
                    course.thumbnail.url
                )

            # -------------------------------------------------
            # ADD TO CONTINUE LEARNING
            # -------------------------------------------------

            continue_learning.append(
                {
                    "course_id": course.id,
                    "course_title": course.title,
                    "course_slug": course.slug,

                    # First incomplete lesson
                    "lesson_id": (
                        next_lesson.id
                        if next_lesson
                        else None
                    ),

                    "thumbnail": thumbnail,

                    "progress": progress,

                    "completed_lessons": completed_count,

                    "total_lessons": lessons_count,

                    "course_completed": course_completed,
                }
            )

        # =====================================================
        # RESPONSE
        # =====================================================

        return Response(
            {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "profile_image": (
                        request.build_absolute_uri(
                            user.profile_image.url
                        )
                        if user.profile_image
                        else None
                    ),
                },

                "total_courses": total_courses,
                "completed_courses": completed_courses,
                "in_progress_courses": in_progress_courses,
                "total_lessons": total_lessons,
                "completed_lessons": completed_lessons,
                "overall_progress": overall_progress,
                "continue_learning": continue_learning,
            }
        )