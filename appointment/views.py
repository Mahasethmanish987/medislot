from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from doctor.models import DoctorProfile, Slot
from .models import Appointment
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
def book_appointment(request, slot_id):
    
    
    
    if request.method == 'POST':
        # Use a database transaction with row-level lock

     try: 
        with transaction.atomic():
            # Lock the slot row for update (prevents concurrent modifications)
            slot = Slot.objects.select_for_update().get(pk=slot_id)
            if slot.no_of_quota_remaining <= 0:
                messages.error(request, "This slot is no longer available.")
                return redirect('doctor:doctor_public_profile', pk=slot.doctor.id)
            queue_number = slot.total_quota - slot.no_of_quota_remaining + 1
            appointment = Appointment.objects.create(
                doctor=slot.doctor,
                patient=request.user,
                date=slot.date,
                start_time=slot.start_time,
                end_time=slot.end_time,
                queue_number=queue_number,
                status='pending'
            )
            
            # Decrease quota
            slot.no_of_quota_remaining -= 1
            slot.save()
            messages.success(request, f"Appointment booked! Queue number: {queue_number}")
        return redirect('appointment:detail', pk=appointment.pk)
     except Exception as e:
         messages.error(request, f"An error occurred while booking the appointment: {str(e)}")
         return redirect('doctor:doctor_public_profile', pk=slot.doctor.id)
     
    slot = get_object_or_404(Slot, pk=slot_id)
    context = {
        'slot': slot,
        'doctor': slot.doctor,
        'patient': request.user,
    }
    return render(request, 'appointment/book_confirmation.html', context)        
    
    

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    # Only the patient, the doctor, or a superuser can view
    if request.user == appointment.patient or request.user == appointment.doctor.user or request.user.is_superuser:
        context = {'appointment': appointment}
        return render(request, 'appointment/appointment_detail.html', context)
    else:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You are not allowed to view this appointment.")   

@login_required
@require_POST
def update_appointment_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    if appointment.doctor.user != request.user:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    new_status = request.POST.get('status')
    if new_status not in ['pending', 'completed', 'cancelled']:
        return JsonResponse({'success': False, 'error': 'Invalid status value'}, status=400)
    
    appointment.status = new_status
    appointment.save()
    
    # Manually map status to display string (in case choices are missing)
    status_display = {
        'pending': 'Pending',
        'completed': 'Completed',
        'cancelled': 'Cancelled',
    }.get(new_status, new_status.capitalize())
    
    return JsonResponse({
        'success': True,
        'new_status': new_status,
        'new_status_display': status_display,
        'message': f'Status updated to {status_display}'
    })