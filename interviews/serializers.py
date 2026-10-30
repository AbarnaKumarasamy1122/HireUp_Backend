from rest_framework import serializers
from .models import Interview


class InterviewSerializer(serializers.ModelSerializer):

    candidate_name = serializers.CharField(
        source="candidate.first_name",
        read_only=True
    )

    candidate_email = serializers.CharField(
        source="candidate.email",
        read_only=True
    )

    job_title = serializers.CharField(
        source="job.title",
        read_only=True
    )

    class Meta:

        model = Interview

        fields = [
            "id",
            "application",
            "candidate",
            "candidate_name",
            "candidate_email",
            "company",
            "job",
            "job_title",
            "scheduled_at",
            "meeting_link",
            "status",
            "created_at",
        ]