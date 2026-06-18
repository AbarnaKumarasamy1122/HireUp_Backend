# from rest_framework import serializers
# from .models import Application


# class ApplicationSerializer(serializers.ModelSerializer):

#     job_title = serializers.CharField(
#         source="job.title",
#         read_only=True
#     )

#     company_name = serializers.CharField(
#         source="job.company.company_name",
#         read_only=True
#     )

#     class Meta:
#         model = Application
#         fields = "__all__"

from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):

    # Candidate details
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

    resume_url = serializers.CharField(
        source="candidate.resume_url",
        read_only=True
    )

    # Job details
    job_title = serializers.CharField(
        source="job.title",
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
            "id",

            # candidate
            "first_name",
            "last_name",
            "email",
            "resume_url",

            # job
            "job_title",
            "job_description",
            "location_type",
            "salary",
            "deadline",

            # application
            "cover_letter",
            "address",
            "contact_number",
            "degree",
            "expected_salary",
            "experience",
            "skills",
            "status",
            "created_at",
        ]