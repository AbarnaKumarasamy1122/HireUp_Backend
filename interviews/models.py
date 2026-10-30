from django.db import models
from users.models import User
from jobs.models import Job
from applications.models import Application

class Interview(models.Model):

    STATUS_CHOICES = (
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="interview"
    )

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="interviews"
    )

    company = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="company_interviews"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    scheduled_at = models.DateTimeField()

    meeting_link = models.URLField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.candidate.email} - "
            f"{self.job.title}"
        )