from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from courses.models import Category, Course
from enrollments.models import Enrollment
from .models import Section, Lesson, LessonProgress, Quiz, QuizAttempt

class LessonAccessSecurityTests(TestCase):
    def setUp(self):

        User = get_user_model()

        self.instructor = User.objects.create_user(
        username="instructor_test",
        email="instructor_test@example.com",
        password="test-password-123",
    )

        self.student = User.objects.create_user(
            username="student_test",
            email="student_test@example.com",
            password="test-password-123",
        )

        self.other_student = User.objects.create_user(
            username="other_student_test",
            email="other_student_test@example.com",
            password="test-password-123",
        )

        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
        )

        self.course = Course.objects.create(
            instructor=self.instructor,
            category=self.category,
            title="Test Paid Course",
            slug="test-paid-course",
            short_description="Test course",
            description="Course for security tests",
            price=499,
            is_published=True,
        )

        self.section = Section.objects.create(
            course=self.course,
            title="Test Section",
            order=1,
        )

        self.preview_lesson = Lesson.objects.create(
            section=self.section,
            title="Preview Lesson",
            description="Public preview",
            video_url="https://example.com/preview",
            is_published=True,
            is_preview=True,
            order=1,
        )

        self.paid_lesson = Lesson.objects.create(
            section=self.section,
            title="Paid Lesson",
            description="Protected lesson",
            video_url="https://example.com/paid",
            is_published=True,
            is_preview=False,
            order=2,
        )

        self.quiz = Quiz.objects.create(
            lesson=self.paid_lesson,
            title="Paid Lesson Quiz",
        )

        self.client = APIClient()

    def test_anonymous_user_can_access_preview_lesson(self):
        response = self.client.get(
            f"/api/lessons/{self.preview_lesson.id}/"
        )

        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cannot_access_paid_lesson_detail(self):
        response = self.client.get(
            f"/api/lessons/{self.paid_lesson.id}/"
        )

        self.assertIn(response.status_code, (403, 404))

    def test_curriculum_hides_locked_lesson_content(self):
        response = self.client.get(
            f"/api/lessons/courses/{self.course.id}/curriculum/"
        )

        self.assertEqual(response.status_code, 200)

        lessons = [
            lesson
            for section in response.data
            for lesson in section["lessons"]
        ]

        paid_lesson = next(
            lesson
            for lesson in lessons
            if lesson["id"] == self.paid_lesson.id
        )

        self.assertIsNone(paid_lesson["video_url"])
        self.assertIsNone(paid_lesson["notes_url"])
        self.assertIsNone(paid_lesson["quiz"])
        self.assertFalse(paid_lesson["has_quiz"])

    def test_non_enrolled_user_cannot_access_quiz(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.get(
            f"/api/lessons/{self.paid_lesson.id}/quiz/"
        )

        self.assertIn(response.status_code, (403, 404))

    def test_non_enrolled_user_cannot_create_progress(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.post(
            "/api/lessons/progress/",
            {
                "lesson": self.paid_lesson.id,
                "completed": False,
                "watched_percentage": 10,
            },
            format="json",
        )

        self.assertIn(response.status_code, (403, 404))

        self.assertFalse(
            LessonProgress.objects.filter(
                user=self.student,
                lesson=self.paid_lesson,
            ).exists()
        )

    def test_non_enrolled_user_cannot_update_progress_to_paid_lesson(self):
        progress = LessonProgress.objects.create(
            user=self.student,
            lesson=self.preview_lesson,
            watched_percentage=25,
        )

        self.client.force_authenticate(user=self.student)

        response = self.client.patch(
            f"/api/lessons/progress/{progress.id}/",
            {
                "lesson": self.paid_lesson.id,
                "watched_percentage": 50,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)

        progress.refresh_from_db()
        self.assertEqual(progress.lesson_id, self.preview_lesson.id)
        self.assertEqual(progress.watched_percentage, 25)



    def test_user_cannot_read_another_users_progress(self):
        progress = LessonProgress.objects.create(
            user=self.other_student,
            lesson=self.preview_lesson,
            watched_percentage=25,
        )

        self.client.force_authenticate(user=self.student)

        response = self.client.get(
            f"/api/lessons/progress/{progress.id}/"
        )

        self.assertEqual(response.status_code, 404)

    def test_enrolled_user_can_access_paid_lesson(self):
        Enrollment.objects.create(
            user=self.student,
            course=self.course,
            is_active=True,
        )

        self.client.force_authenticate(user=self.student)

        response = self.client.get(
            f"/api/lessons/{self.paid_lesson.id}/"
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.data["video_url"],
            self.paid_lesson.video_url,
        )

    def test_non_enrolled_user_cannot_submit_quiz(self):
        self.client.force_authenticate(user=self.student)

        attempts_before = QuizAttempt.objects.count()

        response = self.client.post(
            f"/api/lessons/quizzes/{self.quiz.id}/submit/",
            {"answers": []},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            QuizAttempt.objects.count(),
            attempts_before,
        )