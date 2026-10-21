from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Category, Course
from .models import Enrollment


User = get_user_model()


class EnrollmentAPITests(APITestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="TestPass123!",
        )
        self.other_student = User.objects.create_user(
            username="student2",
            email="student2@example.com",
            password="TestPass123!",
        )
        self.instructor = User.objects.create_user(
            username="teacher1",
            email="teacher1@example.com",
            password="TestPass123!",
            role="teacher",
        )

        self.category = Category.objects.create(
            name="Programming",
            slug="programming",
        )

        self.free_course = Course.objects.create(
            instructor=self.instructor,
            category=self.category,
            title="Free Python",
            slug="free-python",
            short_description="Free course for testing",
            description="Testing free enrollment",
            price=Decimal("0.00"),
            is_published=True,
        )

        self.paid_course = Course.objects.create(
            instructor=self.instructor,
            category=self.category,
            title="Paid Python",
            slug="paid-python",
            short_description="Paid course for testing",
            description="Testing paid enrollment",
            price=Decimal("499.00"),
            is_published=True,
        )

        self.unpublished_course = Course.objects.create(
            instructor=self.instructor,
            category=self.category,
            title="Draft Python",
            slug="draft-python",
            short_description="Unpublished course",
            description="Testing unpublished course",
            price=Decimal("0.00"),
            is_published=False,
        )

        self.url = reverse("enrollment-list")

    def test_anonymous_user_cannot_enroll(self):
        response = self.client.post(
            self.url,
            {"course": self.free_course.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(Enrollment.objects.count(), 0)

    def test_student_can_enroll_in_free_course(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.post(
            self.url,
            {"course": self.free_course.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.data,
        )
        self.assertTrue(
            Enrollment.objects.filter(
                user=self.student,
                course=self.free_course,
            ).exists()
        )

    def test_paid_course_enrollment_is_rejected(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.post(
            self.url,
            {"course": self.paid_course.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            response.data,
        )
        self.assertFalse(
            Enrollment.objects.filter(
                user=self.student,
                course=self.paid_course,
            ).exists()
        )

    def test_duplicate_enrollment_is_rejected(self):
        Enrollment.objects.create(
            user=self.student,
            course=self.free_course,
        )
        self.client.force_authenticate(user=self.student)

        response = self.client.post(
            self.url,
            {"course": self.free_course.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            response.data,
        )
        self.assertEqual(
            Enrollment.objects.filter(
                user=self.student,
                course=self.free_course,
            ).count(),
            1,
        )

    def test_student_cannot_enroll_in_unpublished_course(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.post(
            self.url,
            {"course": self.unpublished_course.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            response.data,
        )
        self.assertFalse(
            Enrollment.objects.filter(
                user=self.student,
                course=self.unpublished_course,
            ).exists()
        )

    def test_student_can_only_list_own_enrollments(self):
        Enrollment.objects.create(
            user=self.student,
            course=self.free_course,
        )
        Enrollment.objects.create(
            user=self.other_student,
            course=self.paid_course,
        )
        self.client.force_authenticate(user=self.student)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.data,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["course"],
            self.free_course.id,
        )
