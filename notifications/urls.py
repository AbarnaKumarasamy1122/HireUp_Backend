from django.urls import path
from .views import admin_notifications, my_notifications

urlpatterns = [
    path("my-notifications/", my_notifications),
    path("admin-notifications/", admin_notifications),
]