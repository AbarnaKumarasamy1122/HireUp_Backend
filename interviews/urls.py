from django.urls import path

from .views import (
    schedule_interview,
    company_interviews,
    my_interviews,
    complete_interview,
    update_interview,
)


urlpatterns = [

    path(
        "schedule-interview/",
        schedule_interview
    ),

    path(
        "company-interviews/",
        company_interviews
    ),

    path(
        "my-interviews/",
        my_interviews
    ),

    path(
        "complete-interview/<int:id>/",
        complete_interview
    ),

    path(
        "update-interview/<int:id>/",
        update_interview
    ),
]