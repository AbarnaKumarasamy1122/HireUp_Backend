from django.urls import path
from .views import my_interviews

urlpatterns = [
    path("my-interviews/", my_interviews),
]