from django.urls import path
from .views import register_user, login_user, send_otp, reset_password 

urlpatterns = [
    path("register/", register_user),
    path("login/", login_user),
    path("send-otp/", send_otp),
    path("reset-password/", reset_password),
]