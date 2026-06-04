from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ("candidate", "Candidate"),
        ("employer", "Employer"),
        ("admin", "Admin"),
    )

    username = models.CharField(
        max_length=255,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="candidate"
    )

    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    profile_image = models.URLField(
        blank=True,
        null=True
    )

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email