from django.urls import path
from .views import admin_profile, all_companies, approve_company, candidate_profile, company_profile, pending_companies, register_user, login_user, reject_company, send_otp, reset_password, update_admin_profile 

urlpatterns = [
    path("register/", register_user),
    path("login/", login_user),
    path("send-otp/", send_otp),
    path("reset-password/", reset_password),
    path("pending-companies/", pending_companies),
    path("approve-company/<int:id>/", approve_company),
    path("reject-company/<int:id>/", reject_company),
    path("all-companies/", all_companies),
    path("admin-profile/<int:id>/", admin_profile),
    path("update-admin-profile/<int:id>/", update_admin_profile),
    path("<int:id>/company-profile/", company_profile),
    path("<int:id>/candidate-profile/", candidate_profile),
]