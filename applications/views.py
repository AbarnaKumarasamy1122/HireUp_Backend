from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Application
from .serializers import ApplicationSerializer
from jobs.models import Job

# APPLY JOB
# APPLY JOB
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def apply_job(request):

    if request.user.role != "candidate":
        return Response(
            {"error": "Only candidates can apply"},
            status=400
        )

    job_id = request.data.get("job_id")

    if not job_id:
        return Response(
            {"error": "Job ID is required"},
            status=400
        )

    if Application.objects.filter(
        candidate=request.user,
        job_id=job_id
    ).exists():
        return Response(
            {"error": "Already applied"},
            status=400
        )

    # Resume validation
    resume_url = request.data.get("resume_url")

    if not resume_url:
        return Response(
            {"error": "Please upload your resume before applying"},
            status=400
        )

    application = Application.objects.create(
        candidate=request.user,
        job_id=job_id,

        cover_letter=request.data.get("cover_letter"),
        resume_url=resume_url,

        experience=request.data.get("experience"),
        degree=request.data.get("degree"),
        expected_salary=request.data.get("expected_salary"),

        contact_number=request.data.get("contact_number"),
        address=request.data.get("address"),
        skills=request.data.get("skills"),
    )

    return Response(
        ApplicationSerializer(application).data
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def applied_job_ids(request):

    ids = Application.objects.filter(
        candidate=request.user
    ).values_list(
        "job_id",
        flat=True
    )

    return Response(list(ids))

# MY APPLICATIONS
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_applications(request):
    apps = Application.objects.filter(candidate=request.user).order_by("-created_at")
    return Response(ApplicationSerializer(apps, many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def company_applications(request, id):

    if request.user.role != "company":
        return Response(
            {"error": "Only companies can view applicants"},
            status=403
        )


    applications = Application.objects.filter(
        job__company_id=id
    ).select_related(
        "candidate",
        "job"
    ).order_by("-created_at")


    serializer = ApplicationSerializer(
        applications,
        many=True
    )

    return Response(serializer.data)