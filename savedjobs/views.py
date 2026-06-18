from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import SavedJob
from .serializers import SavedJobSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_saved_jobs(request):
    jobs = SavedJob.objects.filter(user=request.user).order_by("-created_at")
    return Response(SavedJobSerializer(jobs, many=True).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_job(request):

    job_id = request.data.get("job_id")

    saved, created = SavedJob.objects.get_or_create(
        user=request.user,
        job_id=job_id
    )

    if not created:
        return Response({
            "message": "Already saved"
        })

    return Response(
        SavedJobSerializer(saved).data
    )

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_saved_job(request, job_id):

    SavedJob.objects.filter(
        user=request.user,
        job_id=job_id
    ).delete()

    return Response({
        "message": "Removed"
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def saved_job_ids(request):

    ids = SavedJob.objects.filter(
        user=request.user
    ).values_list(
        "job_id",
        flat=True
    )

    return Response(list(ids))