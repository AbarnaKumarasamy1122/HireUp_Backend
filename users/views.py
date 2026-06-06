from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from django.core.mail import send_mail

from imagekitio import ImageKit

import os
import random

from .models import User, PasswordResetOTP
from .serializers import UserSerializer

# =========================
# IMAGEKIT
# =========================

imagekit = ImageKit(
    public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
    url_endpoint=os.getenv("IMAGEKIT_URL_ENDPOINT"),
)

@api_view(["GET"])
def imagekit_auth(request):

    authentication_parameters = (
        imagekit.get_authentication_parameters()
    )

    return Response(authentication_parameters)


# =========================
# REGISTER
# =========================
@api_view(["POST"])
def register_user(request):

    data = request.data

    email = data.get("email")

    if User.objects.filter(email=email).exists():

        return Response(
            {"error": "Email already exists"},
            status=400
        )
    
    role = data.get("role")

    user = User.objects.create_user(

        username=email,
        email=email,
        password=data.get("password"),

        first_name=data.get("first_name", ""),
        last_name=data.get("last_name", ""),

        role=role,

        # COMPANY DETAILS
        company_name=data.get("company_name"),
        company_address=data.get("company_address"),
        company_contact=data.get("company_contact"),
        company_website=data.get("company_website"),
        company_description=data.get("company_description"),
        verified_document=data.get("verified_document"),

        company_status="pending" if role == "company" else "approved"
    )

    return Response({
        "message": "Registration successful. Wait for admin approval."
    })



# =========================
# LOGIN
# =========================
@api_view(["POST"])
def login_user(request):

    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(
        username=email,
        password=password
    )

    if not user:
        return Response(
            {"error": "Invalid credentials"},
            status=401
        )

    # COMPANY APPROVAL CHECK
    if user.role == "company" :
        if user.company_status == "pending":
            return Response(
                {"error": "Company is waiting for admin approval"},
                status=403
        )

        if user.company_status == "rejected":
            return Response(
                {"error": "Company account is rejected by admin"},
                status=403
        )

    refresh = RefreshToken.for_user(user)

    return Response({

        "token": str(refresh.access_token),

        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,

            "company_name": user.company_name,
            "company_address": user.company_address,
            "company_contact": user.company_contact,
            "company_website": user.company_website,
            "company_description": user.company_description,
            "verified_document": user.verified_document,
            "company_status": user.company_status,

            "profile_image": user.profile_image,
        }
    })

# =========================
# GET PENDING COMPANIES
# =========================
@api_view(["GET"])
def pending_companies(request):

    companies = User.objects.filter(
        role="company",
        company_status="pending"
    )

    serializer = UserSerializer(
        companies,
        many=True
    )

    return Response(serializer.data)


# =========================
# APPROVE COMPANY
# =========================
@api_view(["PUT"])
def approve_company(request, id):

    company = User.objects.get(id=id)

    company.company_status = "approved"

    company.save()

    return Response({
        "message": "Company approved successfully"
    })

# =========================
# REJECT COMPANY
# =========================
@api_view(["PUT"])
def reject_company(request, id):

    company = User.objects.get(id=id)
    company.company_status = "rejected"
    company.save()

    return Response({"message": "Company rejected"})

# =========================
# GET ALL COMPANIES
# =========================

@api_view(["GET"])
def all_companies(request):

    companies = User.objects.filter(role="company")

    serializer = UserSerializer(companies, many=True)

    return Response(serializer.data)

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
        company_status=False
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


# users/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# =========================
# GET ADMIN PROFILE
# =========================
@api_view(["GET"])
def admin_profile(request, id):

    try:
        admin = User.objects.get(
            id=id,
            role="admin"
        )

        serializer = UserSerializer(admin)

        return Response(serializer.data)

    except User.DoesNotExist:
        return Response(
            {"error": "Admin not found"},
            status=404
        )


# =========================
# UPDATE ADMIN PROFILE
# =========================
@api_view(["PUT"])
def update_admin_profile(request, id):

    try:
        admin = User.objects.get(
            id=id,
            role="admin"
        )

        admin.first_name = request.data.get(
            "first_name",
            admin.first_name
        )

        admin.last_name = request.data.get(
            "last_name",
            admin.last_name
        )

        admin.profile_image = request.data.get(
            "profile_image",
            admin.profile_image
        )

        admin.save()

        serializer = UserSerializer(admin)

        return Response({
            "message": "Profile updated successfully",
            "user": serializer.data
        })

    except User.DoesNotExist:
        return Response(
            {"error": "Admin not found"},
            status=404
        )