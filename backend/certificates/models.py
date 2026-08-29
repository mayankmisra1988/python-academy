from django.conf import settings
from django.db import models

from courses.models import Course
from django.utils import timezone

class Certificate(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="certificates",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="certificates",
    )

    certificate_id = models.CharField(
        max_length=50,
        unique=True,
    )

    pdf = models.FileField(
        upload_to="certificates/",
        blank=True,
        null=True,
    )

    issued_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-issued_at"]
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            year = timezone.now().year

            last_certificate = (
                Certificate.objects.filter(
                    certificate_id__startswith=f"PYA-{year}"
                )
                .order_by("-id")
                .first()
            )

            if last_certificate:

                last_number = int(
                    last_certificate.certificate_id.split("-")[-1]
                ) + 1
            else:
                last_number = 1

            self.certificate_id = (
                f"PYA-{year}-{last_number:06d}"
            )
        super().save(*args, **kwargs)