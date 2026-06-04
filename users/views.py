from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

import random

from .models import User, PasswordResetOTP


# =========================
# REGISTER
# =========================
@api_view(["POST"])
def register_user(request):
    data = request.data
    email = data.get("email")

    if not email:
        return Response({"error": "Email is required"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=400)

    user = User.objects.create_user(
        username=email,
        email=email,
        password=data.get("password"),
        first_name=data.get("first_name", ""),
        last_name=data.get("last_name", ""),
        role=data.get("role", "candidate"),
        company_name=data.get("company_name", None),
    )

    return Response({
        "message": "User created successfully",
        "role": user.role
    })


# =========================
# LOGIN
# =========================
@api_view(["POST"])
def login_user(request):

    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email and password required"}, status=400)

    user = authenticate(username=email, password=password)

    if not user:
        return Response({"error": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)

    return Response({
        "token": str(refresh.access_token),
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "company_name": user.company_name,
            "profile_image": user.profile_image,
        }
    })


# =========================
# SEND OTP (FIXED)
# =========================
@api_view(["POST"])
def send_otp(request):

    email = request.data.get("email")

    if not email:
        return Response(
            {"error": "Email is required"},
            status=400
        )

    if not User.objects.filter(email=email).exists():
        return Response(
            {"error": "User not found"},
            status=404
        )

    otp = str(random.randint(100000, 999999))

    PasswordResetOTP.objects.create(
        email=email,
        otp=otp
    )

    send_mail(
        "HireUp Password Reset OTP",
        f"Your OTP is {otp}. Valid for 10 minutes.",
        "noreply@hireup.com",
        [email],
        fail_silently=False,
    )

    return Response({"message": "OTP sent"})


# =========================
# RESET PASSWORD (FIXED)
# =========================
@api_view(["POST"])
def reset_password(request):

    email = request.data.get("email")
    otp = request.data.get("otp")
    new_password = request.data.get("new_password")

    if not email or not otp or not new_password:
        return Response(
            {"error": "All fields required"},
            status=400
        )

    record = PasswordResetOTP.objects.filter(
        email=email,
        otp=otp,
        is_used=False
    ).first()

    if not record:
        return Response({"error": "Invalid OTP"}, status=400)

    if record.is_expired():
        return Response({"error": "OTP expired"}, status=400)

    user = User.objects.filter(email=email).first()

    if not user:
        return Response({"error": "User not found"}, status=404)

    user.set_password(new_password)
    user.save()

    record.is_used = True
    record.save()

    return Response({"message": "Password updated successfully"})