from django.shortcuts import render

from django.test import TestCase
from .models import DoctorProfile, Department, SlotTemplate, Slot
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from .models import DoctorProfile, Slot
# Create your tests here.
def get_doctor_profile(request):

    query = request.GET.get("q","")
    doctors = DoctorProfile.objects.all().order_by("id")
    if query: 
       doctors = DoctorProfile.objects.filter(Q(department__name__icontains=query) | Q(user__first_name__icontains=query)).order_by("id")
    paginator = Paginator(doctors, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "doctor/doctor_list.html", {"q":query, "page_obj": page_obj})
       

   
def doctor_search(request): 
    return render(request, "doctor/doctor_search.html")

def doctor_dashboard(request):

    current_datetime = timezone.now()
    start_time = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = current_datetime.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    return render(request, "doctor/doctor_dashboard.html")

def doctor_public_profile(request, pk):

    doctor = get_object_or_404(DoctorProfile, pk=pk)
    
    now = timezone.localtime(timezone.now())  
    today = now.date()
    future_date_limit = today + timedelta(days=7)
    
    # Get future slots up to 7 days ahead
    slots_qs = Slot.objects.filter(
        doctor=doctor,
        date__gte=today,
        date__lte=future_date_limit,
        no_of_quota_remaining__gt=0
    ).order_by('date', 'start_time')
    available_slots = []
    for slot in slots_qs:
        if slot.date == today:
           
            slot_dt = datetime.combine(today, slot.start_time)
            
            if slot_dt > now:
                available_slots.append(slot)
        else:
            available_slots.append(slot)
    
    context = {
        'doctor': doctor,
        'available_slots': available_slots,
    }
    return render(request, 'doctor/doctor_profile.html', context)