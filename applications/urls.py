from django.urls import path
from .views import apply_job, my_applications, applied_job_ids, company_applications

urlpatterns = [
    path("apply-job/", apply_job),
    path("applied-job-ids/", applied_job_ids),
    path("candidate-applications/", my_applications),
    path("company-applications/<int:id>/", company_applications),
]