from django.db import models
from jobs.models import Job
from users.models import User


class Application(models.Model):

    STATUS = (
        ("pending", "Pending"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("accepted", "Accepted"),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    degree = models.CharField(max_length=255)
    experience = models.CharField(max_length=100)

    salary_expectation = models.CharField(max_length=100)

    cover_letter = models.TextField(blank=True, null=True)

    upload_cv = models.FileField(upload_to="cvs/")

    status = models.CharField(max_length=20, choices=STATUS, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)