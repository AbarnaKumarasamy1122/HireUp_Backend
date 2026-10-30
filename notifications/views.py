from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_notifications(request):
    notes = Notification.objects.filter(user=request.user).order_by("-created_at")
    return Response(NotificationSerializer(notes, many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin_notifications(request):
    if request.user.role != "admin":
        return Response({"error": "Only admins can view these notifications"}, status=403)

    notes = Notification.objects.filter(user=request.user).order_by("-created_at")[:30]
    return Response(NotificationSerializer(notes, many=True).data)