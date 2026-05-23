from django.db import models
from accounts.models import User
from doctor.models import DoctorProfile

class Appointment(models.Model): 
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    doctor=models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, related_name="appointments",null=True,blank=True)
    patient=models.ForeignKey(User, on_delete=models.SET_NULL, related_name="appointments",null=True,blank=True)
    date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    queue_number=models.PositiveIntegerField(editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    class Meta: 
        ordering = ['-date', 'start_time', 'queue_number']
        unique_together = ["doctor", "patient","date"]   