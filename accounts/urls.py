from django.urls import path 
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('redirect/', views.user_redirect, name='user_redirect'),
    path('patient-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
]