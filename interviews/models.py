from django.db import models
from users.models import User
from jobs.models import Job


class Interview(models.Model):

    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interviews")
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="company_interviews")
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    scheduled_at = models.DateTimeField()
    meeting_link = models.URLField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("scheduled", "Scheduled"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="scheduled"
    )

    created_at = models.DateTimeField(auto_now_add=True)