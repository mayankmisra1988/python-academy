from datetime import timedelta
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from certificates.models import Certificate
from courses.models import Category, Course
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
from .views import update_course_completion

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
        self.assertEqual(QuizAttempt.objects.count(), attempts_before)

    def test_empty_quiz_submission_is_rejected_without_creating_attempt(self):
        Enrollment.objects.create(
            user=self.student,
            course=self.course,
            is_active=True,
        )
        self.client.force_authenticate(user=self.student)

        attempts_before = QuizAttempt.objects.count()

        response = self.client.post(
            f"/api/lessons/quizzes/{self.quiz.id}/submit/",
            {"answers": []},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            QuizAttempt.objects.count(),
            attempts_before,
        )


    def test_cannot_complete_quiz_lesson_without_passing_quiz(self):
        Enrollment.objects.create(
            user=self.student,
            course=self.course,
            is_active=True,
        )
        self.client.force_authenticate(user=self.student)

        response = self.client.post(
            "/api/lessons/progress/",
            {
                "lesson": self.paid_lesson.id,
                "completed": True,
                "watched_percentage": 100,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            LessonProgress.objects.filter(
                user=self.student,
                lesson=self.paid_lesson,
                completed=True,
            ).exists()
        )

    def test_course_completion_requires_passing_all_active_quizzes(self):
        enrollment = Enrollment.objects.create(
            user=self.student,
            course=self.course,
            is_active=True,
        )

        LessonProgress.objects.create(
            user=self.student,
            lesson=self.preview_lesson,
            completed=True,
            watched_percentage=100,
        )
        LessonProgress.objects.create(
            user=self.student,
            lesson=self.paid_lesson,
            completed=True,
            watched_percentage=100,
        )

        update_course_completion(self.student, self.course)
        enrollment.refresh_from_db()
        self.assertFalse(enrollment.completed)

        QuizAttempt.objects.create(
            student=self.student,
            quiz=self.quiz,
            total_questions=1,
            correct_answers=1,
            score=100,
            percentage=100,
            passed=True,
        )

        update_course_completion(self.student, self.course)
        enrollment.refresh_from_db()
        self.assertTrue(enrollment.completed)
        self.assertIsNotNone(enrollment.completed_at)

    def test_failed_quiz_does_not_complete_lesson_or_course(self):
        enrollment = Enrollment.objects.create(
            user=self.student,
            course=self.course,
            is_active=True,
        )

        question = Question.objects.create(
            quiz=self.quiz,
            question="What is Python?",
            order=1,
        )
        Option.objects.create(
            question=question,
            option_text="Correct answer",
            is_correct=True,
        )
        wrong_option = Option.objects.create(
            question=question,
            option_text="Wrong answer",
            is_correct=False,
        )

        self.client.force_authenticate(user=self.student)

        response = self.client.post(
            f"/api/lessons/quizzes/{self.quiz.id}/submit/",
            {
                "answers": [
                    {
                        "question": question.id,
                        "option": wrong_option.id,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.data["passed"])

        self.assertTrue(
            QuizAttempt.objects.filter(
                student=self.student,
                quiz=self.quiz,
                passed=False,
            ).exists()
        )

        self.assertFalse(
            LessonProgress.objects.filter(
                user=self.student,
                lesson=self.paid_lesson,
                completed=True,
            ).exists()
        )

        enrollment.refresh_from_db()
        self.assertFalse(enrollment.completed)
        self.assertIsNone(enrollment.completed_at)

    @patch(
        "lessons.views.generate_certificate_pdf",
        side_effect=OSError("Certificate storage unavailable"),
    )
    def test_pdf_failure_does_not_rollback_course_completion(
        self,
        mock_generate_pdf,
    ):
        enrollment = Enrollment.objects.create(
            user=self.student,
            course=self.course,
            is_active=True,
        )

        # The preview lesson must already be completed.
        LessonProgress.objects.create(
            user=self.student,
            lesson=self.preview_lesson,
            completed=True,
            watched_percentage=100,
        )

        question = Question.objects.create(
            quiz=self.quiz,
            question="What is Python?",
            order=1,
        )
        correct_option = Option.objects.create(
            question=question,
            option_text="A programming language",
            is_correct=True,
        )

        self.client.force_authenticate(user=self.student)

        response = self.client.post(
            f"/api/lessons/quizzes/{self.quiz.id}/submit/",
            {
                "answers": [
                    {
                        "question": question.id,
                        "option": correct_option.id,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["passed"])

        self.assertTrue(
            QuizAttempt.objects.filter(
                student=self.student,
                quiz=self.quiz,
                passed=True,
            ).exists()
        )

        paid_progress = LessonProgress.objects.get(
            user=self.student,
            lesson=self.paid_lesson,
        )
        self.assertTrue(paid_progress.completed)
        self.assertEqual(paid_progress.watched_percentage, 100)

        enrollment.refresh_from_db()
        self.assertTrue(enrollment.completed)
        self.assertIsNotNone(enrollment.completed_at)

        certificate = Certificate.objects.get(
            user=self.student,
            course=self.course,
        )
        self.assertFalse(bool(certificate.pdf))
        self.assertIsNone(response.data["certificate"]["pdf"])

        mock_generate_pdf.assert_called_once()
    @patch(
        "lessons.views.generate_certificate_pdf",
        side_effect=[
            OSError("Certificate storage unavailable"),
            None,
        ],
    )
    def test_certificate_pdf_generation_retries_on_next_passed_quiz(
        self,
        mock_generate_pdf,
    ):
        Enrollment.objects.create(
            user=self.student,
            course=self.course,
            is_active=True,
        )

        LessonProgress.objects.create(
            user=self.student,
            lesson=self.preview_lesson,
            completed=True,
            watched_percentage=100,
        )

        question = Question.objects.create(
            quiz=self.quiz,
            question="What is Python?",
            order=1,
        )
        correct_option = Option.objects.create(
            question=question,
            option_text="A programming language",
            is_correct=True,
        )

        self.client.force_authenticate(user=self.student)

        url = f"/api/lessons/quizzes/{self.quiz.id}/submit/"
        payload = {
            "answers": [
                {
                    "question": question.id,
                    "option": correct_option.id,
                }
            ]
        }

        first_response = self.client.post(
            url,
            payload,
            format="json",
        )

        self.assertEqual(first_response.status_code, 201)
        self.assertTrue(first_response.data["passed"])

        certificate = Certificate.objects.get(
            user=self.student,
            course=self.course,
        )
        self.assertFalse(bool(certificate.pdf))

        second_response = self.client.post(
            url,
            payload,
            format="json",
        )

        self.assertEqual(second_response.status_code, 201)
        self.assertTrue(second_response.data["passed"])

        self.assertEqual(
            Certificate.objects.filter(
                user=self.student,
                course=self.course,
            ).count(),
            1,
        )
        self.assertEqual(mock_generate_pdf.call_count, 2)

    def test_course_completion_preserves_existing_completed_at(self):
        enrollment = Enrollment.objects.create(
            user=self.student,
            course=self.course,
            is_active=True,
            completed=True,
            completed_at=timezone.now() - timedelta(days=2),
        )

        LessonProgress.objects.create(
            user=self.student,
            lesson=self.preview_lesson,
            completed=True,
            watched_percentage=100,
        )
        LessonProgress.objects.create(
            user=self.student,
            lesson=self.paid_lesson,
            completed=True,
            watched_percentage=100,
        )
        QuizAttempt.objects.create(
            student=self.student,
            quiz=self.quiz,
            total_questions=1,
            correct_answers=1,
            score=100,
            percentage=100,
            passed=True,
        )

        original_completed_at = enrollment.completed_at

        update_course_completion(self.student, self.course)

        enrollment.refresh_from_db()

        self.assertTrue(enrollment.completed)
        self.assertEqual(
            enrollment.completed_at,
            original_completed_at,
        )
    def test_patch_cannot_reduce_watched_percentage_of_completed_lesson(self):
        progress = LessonProgress.objects.create(
            user=self.student,
            lesson=self.preview_lesson,
            completed=True,
            watched_percentage=100,
        )

        self.client.force_authenticate(user=self.student)

        response = self.client.patch(
            f"/api/lessons/progress/{progress.id}/",
            {"watched_percentage": 50},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

        progress.refresh_from_db()
        self.assertTrue(progress.completed)
        self.assertEqual(progress.watched_percentage, 100)

    def test_duplicate_question_answers_are_rejected(self):
        Enrollment.objects.create(
            user=self.student,
            course=self.course,
            is_active=True,
        )
        question = Question.objects.create(
            quiz=self.quiz,
            question="What is Python?",
            order=1,
        )
        option = Option.objects.create(
            question=question,
            option_text="A programming language",
            is_correct=True,
        )

        self.client.force_authenticate(user=self.student)
        attempts_before = QuizAttempt.objects.count()

        response = self.client.post(
            f"/api/lessons/quizzes/{self.quiz.id}/submit/",
            {
                "answers": [
                    {"question": question.id, "option": option.id},
                    {"question": question.id, "option": option.id},
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(QuizAttempt.objects.count(), attempts_before)

    def test_question_from_another_quiz_is_rejected(self):
        Enrollment.objects.create(
            user=self.student,
            course=self.course,
            is_active=True,
        )

        another_lesson = Lesson.objects.create(
            section=self.section,
            title="Another Quiz Lesson",
            description="Test lesson",
            video_url="https://example.com/another",
            is_published=True,
            is_preview=False,
            order=3,
        )
        another_quiz = Quiz.objects.create(
            lesson=another_lesson,
            title="Another Quiz",
        )
        foreign_question = Question.objects.create(
            quiz=another_quiz,
            question="Foreign question?",
            order=1,
        )
        foreign_option = Option.objects.create(
            question=foreign_question,
            option_text="Foreign option",
            is_correct=True,
        )

        self.client.force_authenticate(user=self.student)
        attempts_before = QuizAttempt.objects.count()

        response = self.client.post(
            f"/api/lessons/quizzes/{self.quiz.id}/submit/",
            {
                "answers": [
                    {
                        "question": foreign_question.id,
                        "option": foreign_option.id,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(QuizAttempt.objects.count(), attempts_before)

    def test_option_from_another_question_is_rejected(self):
        Enrollment.objects.create(
            user=self.student,
            course=self.course,
            is_active=True,
        )
        question = Question.objects.create(
            quiz=self.quiz,
            question="What is Python?",
            order=1,
        )
        another_question = Question.objects.create(
            quiz=self.quiz,
            question="Which is a number?",
            order=2,
        )
        foreign_option = Option.objects.create(
            question=another_question,
            option_text="42",
            is_correct=True,
        )

        self.client.force_authenticate(user=self.student)
        attempts_before = QuizAttempt.objects.count()

        response = self.client.post(
            f"/api/lessons/quizzes/{self.quiz.id}/submit/",
            {
                "answers": [
                    {
                        "question": question.id,
                        "option": foreign_option.id,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(QuizAttempt.objects.count(), attempts_before)