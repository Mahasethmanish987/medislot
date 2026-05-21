from django.utils import timezone
from datetime import date, timedelta
from doctor.models import DoctorProfile, Slot,SlotTemplate

def generate_slots_for_date(doctor, target_date: date): 

    days_map ={
        "MON": 0,
        "TUE": 1,
        "WED": 2,
        "THU": 3,
        "FRI": 4,
        "SAT": 5,
        "SUN": 6,
    }
    weekday_num = target_date.weekday()
    
    day_key = next((k for k, v in days_map.items() if v == weekday_num),None)
    if not day_key: 
        return 
    
    templates = SlotTemplate.objects.filter(doctor=doctor,day_of_week=day_key, is_active=True)
    for template in templates: 
       
        if not Slot.objects.filter(doctor=doctor, date=target_date, start_time=template.start_time, end_time=template.end_time).exists():
            
            Slot.objects.create(
                doctor=doctor,
                date=target_date,
                start_time=template.start_time,
                end_time=template.end_time,
                no_of_quota_remaining=template.slot_quota
            ) 

def delete_slots_for_date(doctor, target_date: date): 
    Slot.objects.filter(doctor=doctor, date=target_date, is_active=True).update(is_active=False)


def initial_generate_7_days(): 
    start = date.today() + timedelta(days=1)
    end = start + timedelta(days=7)
    doctors = DoctorProfile.objects.filter(is_active=True)
    
    current = start 
    while current <= end: 
        for doctor in doctors: 
            
            generate_slots_for_date(doctor,current)
        current += timedelta(days=1)

def roll_slots_daily(): 
    today = date.today()
    new_day = today + timedelta(days=8)
    old_day = today + timedelta(days=8)
    doctors = DoctorProfile.objects.filter(is_active=True)
    for doctor in doctors: 
        generate_slots_for_date(doctor, new_day)
        delete_slots_for_date(doctor, old_day)
