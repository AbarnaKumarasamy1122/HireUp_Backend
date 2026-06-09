from rest_framework.decorators import api_view
from rest_framework.response import Response

from jobs.models import Job
from applications.models import Application
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def company_analytics(request, company_id):
    return Response({
        "jobs": Job.objects.filter(company_id=company_id).count(),
        "applications": Application.objects.filter(job__company_id=company_id).count(),
        "pending": Application.objects.filter(
            job__company_id=company_id,
            status="pending"
        ).count(),
    })