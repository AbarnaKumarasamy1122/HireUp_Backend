from django.db import models
from users.models import User


class Job(models.Model):

    LOCATION_TYPE = (
        ("remote", "Remote"),
        ("onsite", "Onsite"),
        ("hybrid", "Hybrid"),
    )

    company = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "company"},
        related_name="jobs"
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    location_type = models.CharField(
        max_length=20,
        choices=LOCATION_TYPE
    )

    location = models.CharField(max_length=255, blank=True, null=True)

    salary = models.CharField(max_length=100, blank=True, null=True)

    deadline = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)