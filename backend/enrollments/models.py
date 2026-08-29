from django.conf import settings
from django.db import models
from courses.models import Course


class Enrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-enrolled_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"],
                name="unique_user_course_enrollment",
            )
        ]

        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["course"]),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.course.title}"