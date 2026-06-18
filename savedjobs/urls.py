from django.urls import path
from .views import my_saved_jobs, remove_saved_job, save_job, saved_job_ids

urlpatterns = [
    path(
        "my-saved-jobs/",
        my_saved_jobs
    ),

    path(
        "save-job/",
        save_job
    ),

    path(
        "remove-saved-job/<int:job_id>/",
        remove_saved_job
    ),

    path(
        "saved-job-ids/",
        saved_job_ids
),
]