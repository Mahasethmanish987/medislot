from django.urls import path
from . import views

app_name = 'appointment'

urlpatterns = [
  path('book/<int:slot_id>/', views.book_appointment, name='book_appointment'),
  path('<int:pk>/', views.appointment_detail, name='detail'),
  path('update-appointment-status/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'), 
   
]