from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):

    # IDs
    candidate_id = serializers.IntegerField(
        source="candidate.id",
        read_only=True
    )

    job_id = serializers.IntegerField(
        source="job.id",
        read_only=True
    )


    # Candidate Details
    first_name = serializers.CharField(
        source="candidate.first_name",
        read_only=True
    )

    last_name = serializers.CharField(
        source="candidate.last_name",
        read_only=True
    )

    email = serializers.EmailField(
        source="candidate.email",
        read_only=True
    )


    # Job Details
    job_title = serializers.CharField(
        source="job.title",
        read_only=True
    )

    company_name = serializers.CharField(
        source="job.company.company_name",
        read_only=True
    )

    job_description = serializers.CharField(
        source="job.description",
        read_only=True
    )

    location_type = serializers.CharField(
        source="job.location_type",
        read_only=True
    )

    location = serializers.CharField(
        source="job.location",
        read_only=True
    )

    salary = serializers.CharField(
        source="job.salary",
        read_only=True
    )

    deadline = serializers.DateField(
        source="job.deadline",
        read_only=True
    )


    class Meta:
        model = Application

        fields = [

            # IDs
            "id",
            "candidate_id",
            "job_id",

            # Candidate
            "first_name",
            "last_name",
            "email",

            # Job
            "job_title",
            "company_name",
            "job_description",
            "location_type",
            "location",
            "salary",
            "deadline",

            # Application details
            "resume_url",
            "cover_letter",
            "degree",
            "experience",
            "expected_salary",
            "contact_number",
            "address",
            "skills",

            # Status
            "status",
            "created_at",
        ]