from django.db import models
from accounts.models import User
class Department(models.Model): 
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class DoctorProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='doctors')
    experience_years = models.PositiveIntegerField(default=0)
    qualifications = models.TextField(blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profile_picture = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True) 
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Dr. {self.user.first_name} {self.user.last_name} " 

class SlotTemplate(models.Model):

    DAYS = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
        ("SUN", "Sunday"),
    ]

    doctor = models.ForeignKey(
        "DoctorProfile",
        on_delete=models.CASCADE,
        related_name="slot_templates"
    )

    day_of_week = models.CharField(max_length=3, choices=DAYS)

    start_time = models.TimeField()
    end_time = models.TimeField()

    slot_quota = models.PositiveIntegerField(default=5)  

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor} - {self.day_of_week}"

class Slot(models.Model):
    doctor = models.ForeignKey(
        "DoctorProfile",
        on_delete=models.CASCADE,
        related_name="slots"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_quota=models.PositiveIntegerField(default=5)
    no_of_quota_remaining = models.PositiveIntegerField(default=5)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor} - {self.date} {self.start_time}-{self.end_time}"