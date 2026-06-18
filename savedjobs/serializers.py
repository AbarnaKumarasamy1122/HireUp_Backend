from rest_framework import serializers
from .models import SavedJob


class SavedJobSerializer(serializers.ModelSerializer):

    job_id = serializers.IntegerField(
        source="job.id",
        read_only=True
    )

    title = serializers.CharField(
        source="job.title",
        read_only=True
    )

    description = serializers.CharField(
        source="job.description",
        read_only=True
    )

    company_name = serializers.CharField(
        source="job.company.company_name",
        read_only=True
    )

    location = serializers.CharField(
        source="job.location",
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
        model = SavedJob
        fields = "__all__"