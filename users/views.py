from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User


@api_view(["POST"])
def register_user(request):

    data = request.data

    email = data.get("email")

    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=email,
        email=email,
        password=data.get("password"),

        first_name=data.get("first_name"),
        last_name=data.get("last_name"),

        role=data.get("role"),

        company_name=data.get("company_name"),
    )

    return Response({
        "message": "User created successfully",
        "role": user.role,
    })