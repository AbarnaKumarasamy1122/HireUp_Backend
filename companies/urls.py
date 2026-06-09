from django.urls import path
from .views import company_analytics

urlpatterns = [
    path("analytics/<int:company_id>/", company_analytics),
]