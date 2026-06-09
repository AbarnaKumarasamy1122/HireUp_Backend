from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import Job
from .serializers import JobSerializer
from django.core.mail import send_mail

# POST JOB
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_job(request):

    job = Job.objects.create(
        company=request.user,
        title=request.data["title"],
        description=request.data["description"],
        location_type=request.data["location_type"],
        location=request.data.get("location"),
        salary=request.data.get("salary"),
        deadline=request.data["deadline"]
    )

    return Response(JobSerializer(job).data)


# GET COMPANY JOBS
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def company_jobs(request, company_id):
    jobs = Job.objects.filter(company_id=company_id)
    return Response(JobSerializer(jobs, many=True).data)

# GET SINGLE JOB
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def job_detail(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        return Response(JobSerializer(job).data)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)

# UPDATE JOB
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)

        job.title = request.data.get("title", job.title)
        job.description = request.data.get("description", job.description)
        job.location_type = request.data.get("location_type", job.location_type)
        job.location = request.data.get("location", job.location)
        job.salary = request.data.get("salary", job.salary)
        job.deadline = request.data.get("deadline", job.deadline)

        job.save()

        return Response(JobSerializer(job).data)

    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)
    
# DELETE JOB
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_job(request, job_id):
    Job.objects.get(id=job_id, company=request.user).delete()
    return Response({"message": "Job deleted"})


# JOB COUNT
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def job_stats(request, company_id):
    return Response({
        "jobs": Job.objects.filter(company_id=company_id).count()
    })

# GET ALL JOBS
@api_view(["GET"])
def all_jobs(request):

    jobs = Job.objects.select_related("company").all().order_by("-created_at")

    data = []

    for job in jobs:
        data.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "location": job.location,
            "location_type": job.location_type,
            "salary": job.salary,
            "deadline": job.deadline,
            "created_at": job.created_at,
            "company_name": job.company.company_name,
        })

    return Response(data)