from django.urls import path
from .views import apply_job, company_applications, update_status

urlpatterns = [
    path("apply/", apply_job),
    path("company/<int:company_id>/", company_applications),
    path("update-status/<int:app_id>/", update_status),
]