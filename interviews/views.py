from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Interview
from .serializers import InterviewSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_interviews(request):
    interviews = Interview.objects.filter(candidate=request.user).order_by("-scheduled_at")
    return Response(InterviewSerializer(interviews, many=True).data)