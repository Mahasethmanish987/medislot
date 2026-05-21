from django.urls import path 
from . import views

app_name = "doctor"

urlpatterns = [
    path("get-doctors/", views.get_doctor_profile, name="doctor_list"),
    path("search/", views.doctor_search, name="doctor_search"),
    path("doctor_dashboard/", views.doctor_dashboard, name="dashboard"),
    path('doctor/<int:pk>/', views.doctor_public_profile, name='doctor_public_profile')
]