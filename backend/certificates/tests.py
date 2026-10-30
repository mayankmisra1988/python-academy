
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from courses.models import Category, Course
from enrollments.models import Enrollment
from certificates.models import Certificate
User = get_user_model()

class CertificateEligibilityTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.instructor = User.objects.create_user(
            username="certificate_instructor",
            email="instructor@example.com",
            password="TestPassword123!",
            role="teacher",
        )

        self.student = User.objects.create_user(
            username="certificate_student",
            email="student@example.com",
            password="TestPassword123!",
            role="student",
        )

        self.other_student = User.objects.create_user(
            username="other_certificate_student",
            email="otherstudent@example.com",
            password="TestPassword123!",
            role="student",
        )

        self.category = Category.objects.create(
            name="Certificate Testing",
            slug="certificate-testing",
        )

        self.course = Course.objects.create(
            instructor=self.instructor,
            category=self.category,
            title="Certificate Test Course",
            slug="certificate-test-course",
            short_description="A course for certificate tests",
            description="Testing certificate eligibility.",
            is_published=True,
        )

        self.enrollment = Enrollment.objects.create(
            user=self.student,
            course=self.course,
            is_active=True,
            completed=False,
        )

        self.generate_url = (
            f"/api/certificates/generate/{self.course.id}/"
        )

    def test_certificate_rejected_without_enrollment(self):
        self.client.force_authenticate(user=self.other_student)

        response = self.client.post(self.generate_url)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            Certificate.objects.filter(
                user=self.other_student,
                course=self.course,
            ).exists()
        )

    def test_certificate_rejected_for_inactive_enrollment(self):
        self.enrollment.is_active = False
        self.enrollment.completed = True
        self.enrollment.save()

        self.client.force_authenticate(user=self.student)

        response = self.client.post(self.generate_url)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            Certificate.objects.filter(
                user=self.student,
                course=self.course,
            ).exists()
        )

    def test_certificate_rejected_for_incomplete_course(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.post(self.generate_url)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            Certificate.objects.filter(
                user=self.student,
                course=self.course,
            ).exists()
        )

    @patch("certificates.views.generate_certificate_pdf")
    def test_completed_course_can_receive_certificate(
        self,
        mock_generate_pdf,
    ):
        self.enrollment.completed = True
        self.enrollment.save()

        self.client.force_authenticate(user=self.student)

        response = self.client.post(self.generate_url)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Certificate.objects.filter(
                user=self.student,
                course=self.course,
            ).count(),
            1,
        )
        mock_generate_pdf.assert_called_once()

    @patch("certificates.views.generate_certificate_pdf")
    def test_generating_again_does_not_create_duplicate(
        self,
        mock_generate_pdf,
    ):
        self.enrollment.completed = True
        self.enrollment.save()

        self.client.force_authenticate(user=self.student)

        first_response = self.client.post(self.generate_url)
        second_response = self.client.post(self.generate_url)

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(
            Certificate.objects.filter(
                user=self.student,
                course=self.course,
            ).count(),
            1,
        )
    @patch(
        "certificates.views.generate_certificate_pdf",
        side_effect=OSError("Cloudinary temporarily unavailable"),
    )
    def test_pdf_failure_preserves_certificate_record(
        self,
        mock_generate_pdf,
    ):
        self.enrollment.completed = True
        self.enrollment.save()
        self.client.force_authenticate(user=self.student)

        response = self.client.post(self.generate_url)

        self.assertEqual(response.status_code, 201)
        self.assertIsNone(response.data.get("pdf"))
        self.assertEqual(
            Certificate.objects.filter(
                user=self.student,
                course=self.course,
            ).count(),
            1,
        )
        mock_generate_pdf.assert_called_once()

    @patch("certificates.views.generate_certificate_pdf")
    def test_pdf_generation_is_retried_without_duplicate_certificate(
        self,
        mock_generate_pdf,
    ):
        mock_generate_pdf.side_effect = [
            OSError("Cloudinary temporarily unavailable"),
            None,
        ]

        self.enrollment.completed = True
        self.enrollment.save()
        self.client.force_authenticate(user=self.student)

        first_response = self.client.post(self.generate_url)
        second_response = self.client.post(self.generate_url)

        self.assertEqual(first_response.status_code, 201)
        self.assertIsNone(first_response.data.get("pdf"))
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(mock_generate_pdf.call_count, 2)
        self.assertEqual(
            Certificate.objects.filter(
                user=self.student,
                course=self.course,
            ).count(),
            1,
        )

    def test_student_cannot_view_another_students_certificate(self):
        certificate = Certificate.objects.create(
            user=self.student,
            course=self.course,
        )

        self.client.force_authenticate(user=self.other_student)

        response = self.client.get(
            f"/api/certificates/{certificate.id}/"
        )

        self.assertEqual(response.status_code, 404)

    def test_student_cannot_download_another_students_certificate(self):
        certificate = Certificate.objects.create(
            user=self.student,
            course=self.course,
        )

        self.client.force_authenticate(user=self.other_student)

        response = self.client.get(
            f"/api/certificates/download/{certificate.id}/"
        )

        self.assertEqual(response.status_code, 404)

    def test_certificate_list_only_returns_current_students_records(self):
        own_certificate = Certificate.objects.create(
            user=self.student,
            course=self.course,
        )

        Certificate.objects.create(
            user=self.other_student,
            course=self.course,
        )

        self.client.force_authenticate(user=self.student)

        response = self.client.get("/api/certificates/")

        self.assertEqual(response.status_code, 200)

        returned_ids = {
            item["id"] for item in response.data
        }

        self.assertEqual(returned_ids, {own_certificate.id})

    def test_certificate_can_be_verified_without_login(self):
        certificate = Certificate.objects.create(
            user=self.student,
            course=self.course,
        )

        response = self.client.get(
            f"/api/certificates/verify/"
            f"{certificate.certificate_id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["valid"])
        self.assertEqual(
            response.data["certificate_id"],
            certificate.certificate_id,
        )

    def test_nonexistent_certificate_returns_404(self):
            response = self.client.get(
                "/api/certificates/verify/does-not-exist/"
            )

            self.assertEqual(response.status_code, 404)