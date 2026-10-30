from rest_framework.decorators import (
    api_view,
    permission_classes
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Interview
from .serializers import InterviewSerializer

from applications.models import Application
from django.utils.dateparse import parse_datetime
from notifications.utils import notify_user


# =================================
# Schedule Interview
# =================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def schedule_interview(request):

    if request.user.role != "company":
        return Response({"error": "Only company can schedule interviews"}, status=403)

    application_id = request.data.get("application_id")
    scheduled_at = request.data.get("scheduled_at")
    meeting_link = request.data.get("meeting_link")

    if not application_id or not scheduled_at:
        return Response({"error": "Missing required fields"}, status=400)

    try:
        application = Application.objects.select_related("job", "candidate").get(id=application_id)
    except Application.DoesNotExist:
        return Response({"error": "Application not found"}, status=404)

    if hasattr(application, "interview"):
        return Response({"error": "Interview already scheduled"}, status=400)

    # ✅ FIX: parse datetime safely
    scheduled_at = parse_datetime(scheduled_at)
    if not scheduled_at:
        return Response({"error": "Invalid datetime format"}, status=400)

    interview = Interview.objects.create(
        application=application,
        candidate=application.candidate,
        company=request.user,
        job=application.job,
        scheduled_at=scheduled_at,
        meeting_link=meeting_link
    )
    notify_user(
        application.candidate,
        "Interview scheduled",
        f"An interview for '{application.job.title}' is scheduled for {interview.scheduled_at:%b %d, %Y at %I:%M %p}.",
    )

    application.status = "shortlisted"
    application.save()

    return Response(InterviewSerializer(interview).data)


# =================================
# Company Interviews
# =================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def company_interviews(request):

    interviews = Interview.objects.filter(
        company=request.user
    ).order_by("-scheduled_at")


    return Response(
        InterviewSerializer(
            interviews,
            many=True
        ).data
    )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_interview(request, id):
    if request.user.role != "company":
        return Response({"error": "Only companies can edit interviews"}, status=403)

    try:
        interview = Interview.objects.get(id=id, company=request.user)
    except Interview.DoesNotExist:
        return Response({"error": "Interview not found"}, status=404)

    scheduled_at = request.data.get("scheduled_at")
    meeting_link = request.data.get("meeting_link")

    if not scheduled_at or not meeting_link:
        return Response({"error": "Date, time, and meeting link are required"}, status=400)

    parsed_scheduled_at = parse_datetime(scheduled_at)
    if not parsed_scheduled_at:
        return Response({"error": "Invalid datetime format"}, status=400)

    interview.scheduled_at = parsed_scheduled_at
    interview.meeting_link = meeting_link
    interview.save(update_fields=["scheduled_at", "meeting_link"])
    notify_user(
        interview.candidate,
        "Interview updated",
        f"The interview for '{interview.job.title}' was rescheduled to {interview.scheduled_at:%b %d, %Y at %I:%M %p}.",
    )

    return Response(InterviewSerializer(interview).data)


# =================================
# Candidate Interviews
# =================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_interviews(request):

    interviews = Interview.objects.filter(
        candidate=request.user
    ).order_by("-scheduled_at")


    return Response(
        InterviewSerializer(
            interviews,
            many=True
        ).data
    )


# =================================
# Complete Interview
# =================================

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def complete_interview(request, id):

    try:
        interview = Interview.objects.get(id=id)
    except Interview.DoesNotExist:
        return Response({"error": "Interview not found"}, status=404)

    interview.status = "completed"
    interview.save()
    notify_user(
        interview.candidate,
        "Interview completed",
        f"Your interview for '{interview.job.title}' was marked as completed.",
    )

    return Response(InterviewSerializer(interview).data)