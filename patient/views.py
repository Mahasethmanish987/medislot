from django.shortcuts import render
from appointment.models import Appointment
from doctor.views import get_appointment_for_local_date_for_doctor
from django.utils import timezone


def patient_dashboard(request):
    today = timezone.now().date()
    
    # Get all appointments for this patient (not today only – show upcoming)
    # For simplicity, show upcoming appointments (today and future)
    appointments = Appointment.objects.filter(
        patient=request.user,
        date__gte=today
    ).select_related('doctor', 'doctor__user').order_by('date', 'start_time')
    
    total_count = appointments.count()
    completed_count = appointments.filter(status='completed').count()
    pending_count = appointments.filter(status='pending').count()
    
    context = {
        'appointments': appointments,
        'total_count': total_count,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'today_date': today,
    }
    return render(request, 'patient/patient_dashboard.html', context)