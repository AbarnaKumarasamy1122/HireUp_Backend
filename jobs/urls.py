from django.urls import path
from .views import all_jobs, job_detail, post_job, company_jobs, delete_job, job_stats, update_job

urlpatterns = [
    path("post-job/", post_job),
    path("jobs/<int:company_id>/", company_jobs),
    path("job/<int:job_id>/", job_detail),
    path("update-job/<int:job_id>/", update_job),
    path("delete-job/<int:job_id>/", delete_job),
    path("all-jobs/", all_jobs),
    path("stats/<int:company_id>/", job_stats),
]