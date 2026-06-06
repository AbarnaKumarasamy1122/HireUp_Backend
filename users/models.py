from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):

    ROLE_CHOICES = (
        ("candidate", "Candidate"),
        ("company", "Company"),
        ("admin", "Admin"),
    )

    COMPANY_STATUS = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
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

    # Company
    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    company_address = models.TextField(
        blank=True,
        null=True
    )

    company_contact = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    company_website = models.URLField(
        blank=True,
        null=True
    )

    company_description = models.TextField(
        blank=True,
        null=True
    )

    verified_document = models.URLField(
        blank=True,
        null=True
    )

    company_status = models.CharField(
        max_length=20,
        choices=COMPANY_STATUS,
        default="pending"
    )

    # Candidate
    profile_image = models.URLField(
        blank=True,
        null=True
    )

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class PasswordResetOTP(models.Model):

    email = models.EmailField()

    otp = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_used = models.BooleanField(
        default=False
    )

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)