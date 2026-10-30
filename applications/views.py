from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Application
from .serializers import ApplicationSerializer
from jobs.models import Job
from interviews.models import Interview
from interviews.serializers import InterviewSerializer
from notifications.utils import notify_admins, notify_user

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
    notify_user(
        application.job.company,
        "New job application",
        f"{request.user.first_name} {request.user.last_name} applied for '{application.job.title}'.",
    )
    notify_admins(
        "New application received",
        f"A new application was submitted for '{application.job.title}'.",
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
        return Response({"error": "Only companies can view applicants"}, status=403)

    applications = Application.objects.filter(
        job__company_id=id
    ).select_related(
        "candidate",
        "job"
    ).prefetch_related(
        "interview"
    ).order_by("-created_at")

    data = []
    for app in applications:
        serialized = ApplicationSerializer(app).data

        try:
            serialized["interview"] = InterviewSerializer(app.interview).data
        except:
            serialized["interview"] = None

        data.append(serialized)

    return Response(data)


# ============================
# Shortlist Candidate
# ============================

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def shortlist_candidate(request, application_id):

    try:

        application = Application.objects.get(
            id=application_id,
            job__company=request.user
        )

        application.status = "shortlisted"
        application.save()
        notify_user(
            application.candidate,
            "Application shortlisted",
            f"Your application for '{application.job.title}' was shortlisted.",
        )

        return Response({
            "message": "Candidate shortlisted successfully"
        })

    except Application.DoesNotExist:

        return Response(
            {"error": "Application not found"},
            status=404
        )


# ============================
# Reject Candidate
# ============================

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def reject_candidate(request, application_id):

    try:

        application = Application.objects.get(
            id=application_id,
            job__company=request.user
        )

        application.status = "rejected"
        application.save()
        notify_user(
            application.candidate,
            "Application update",
            f"Your application for '{application.job.title}' was not selected.",
        )

        return Response({
            "message": "Candidate rejected"
        })

    except Application.DoesNotExist:

        return Response(
            {"error": "Application not found"},
            status=404
        )


# ============================
# Accept Candidate
# Only after interview completed
# ============================

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def accept_candidate(request, application_id):

    try:

        application = Application.objects.get(
            id=application_id,
            job__company=request.user
        )

        try:

            interview = Interview.objects.get(
                application=application
            )


            if interview.status != "completed":

                return Response(
                    {
                        "error":
                        "Interview must be completed before acceptance"
                    },
                    status=400
                )


        except Interview.DoesNotExist:

            return Response(
                {
                    "error":
                    "No interview scheduled for this candidate"
                },
                status=400
            )


        application.status = "accepted"

        application.save()
        notify_user(
            application.candidate,
            "Application accepted",
            f"Congratulations! Your application for '{application.job.title}' was accepted.",
        )


        return Response(
            {"message": "Candidate accepted successfully"}
        )


    except Application.DoesNotExist:

        return Response(
            {
                "error": "Application not found"
            },
            status=404
        )