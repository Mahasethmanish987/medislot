from django.urls import path 
from . import views

app_name = "patient"
urlpatterns = [
    path("patient-dashboard/", views.patient_dashboard, name="dashboard"),
]