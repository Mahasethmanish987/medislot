from django.contrib import admin
from .models import Appointment
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'patient', 'date', 'start_time', 'end_time', 'queue_number', 'status')
    list_filter = ('status', 'date')
    search_fields = ('doctor__user__first_name', 'doctor__user__last_name', 'patient__first_name', 'patient__last_name')