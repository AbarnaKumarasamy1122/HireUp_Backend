from django.urls import path
from .views import apply_job, my_applications, applied_job_ids, company_applications, shortlist_candidate, reject_candidate, accept_candidate

urlpatterns = [
    path("apply-job/", apply_job),
    path("applied-job-ids/", applied_job_ids),
    path("candidate-applications/", my_applications),
    path("company-applications/<int:id>/", company_applications),
    path(
        "shortlist-candidate/<int:application_id>/",
        shortlist_candidate
    ),

    path(
        "reject-candidate/<int:application_id>/",
        reject_candidate
    ),

    path(
        "accept-candidate/<int:application_id>/",
        accept_candidate
    ),
]