from rest_framework import serializers
from .models import Interview


class InterviewSerializer(serializers.ModelSerializer):

    job_title = serializers.CharField(source="job.title", read_only=True)

    class Meta:
        model = Interview
        fields = "__all__"