from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Application
from .serializers import ApplicationSerializer


@api_view(["POST"])
def apply_job(request):
    app = Application.objects.create(
        job_id=request.data["job_id"],
        candidate_id=request.data["candidate_id"],
        first_name=request.data["first_name"],
        last_name=request.data["last_name"],
        email=request.data["email"],
        phone=request.data["phone"],
        degree=request.data["degree"],
        experience=request.data["experience"],
        salary_expectation=request.data["salary_expectation"],
        cover_letter=request.data.get("cover_letter"),
        upload_cv=request.FILES.get("upload_cv"),
    )

    return Response(ApplicationSerializer(app).data)


@api_view(["GET"])
def company_applications(request, company_id):
    apps = Application.objects.filter(job__company_id=company_id)
    return Response(ApplicationSerializer(apps, many=True).data)


@api_view(["PUT"])
def update_status(request, app_id):
    app = Application.objects.get(id=app_id)
    app.status = request.data["status"]
    app.save()
    return Response({"message": "Status updated"})