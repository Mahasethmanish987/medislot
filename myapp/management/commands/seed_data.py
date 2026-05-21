from django.core.management.base import BaseCommand
from accounts.models import User
from doctor.models import Department, DoctorProfile, SlotTemplate


class Command(BaseCommand):
    help = "Seed real structured data (30 doctors + 20 patients)"

    def handle(self, *args, **kwargs):

        # ----------------------------
        # CLEAR OLD DATA (OPTIONAL)
        # ----------------------------
        User.objects.filter(email__contains="@medislot.com").delete()

        # ----------------------------
        # DEPARTMENTS
        # ----------------------------
        departments = [
            "Cardiologist",
            "Dermatologist",
            "Neurologist",
            "Orthopedic",
            "Pediatrician",
            "ENT Specialist",
            "General Physician",
        ]

        dept_objs = []
        for d in departments:
            obj, _ = Department.objects.get_or_create(
                name=d,
                defaults={"description": f"{d} specialist in Nepal"}
            )
            dept_objs.append(obj)

        # ----------------------------
        # REALISTIC NEPALI USERS
        # ----------------------------
        doctor_data = [
            ("Manish", "Mahaseth"),
            ("Sujan", "Shrestha"),
            ("Aayush", "Gurung"),
            ("Ramesh", "Thapa"),
            ("Bibek", "KC"),
            ("Prakash", "Adhikari"),
            ("Nabin", "Rai"),
            ("Sagar", "Lama"),
            ("Dipesh", "Sharma"),
            ("Roshan", "Karki"),
            ("Anil", "Tamang"),
            ("Kiran", "Maharjan"),
            ("Sushil", "Bhattarai"),
            ("Raj", "Pandey"),
            ("Bijay", "Chhetri"),
            ("Sandeep", "Shrestha"),
            ("Hari", "Bista"),
            ("Krishna", "Ghimire"),
            ("Rabin", "Joshi"),
            ("Suraj", "Shah"),
            ("Dinesh", "Malla"),
            ("Arjun", "Khadka"),
            ("Prem", "Adhikari"),
            ("Bikash", "Rana"),
            ("Kamal", "Nepal"),
            ("Sunil", "Lama"),
            ("Milan", "Shrestha"),
            ("Gopal", "Acharya"),
            ("Tika", "Koirala"),
            ("Dev", "Poudel"),
        ]

        patient_data = [
            ("Ram", "Shrestha"),
            ("Sita", "Thapa"),
            ("Hari", "Gurung"),
            ("Gita", "Rai"),
            ("Nirmal", "Karki"),
            ("Maya", "Maharjan"),
            ("Deepak", "Bhattarai"),
            ("Sarita", "Sharma"),
            ("Bikram", "Khadka"),
            ("Pooja", "Adhikari"),
            ("Raju", "Lama"),
            ("Sunita", "Bista"),
            ("Ashok", "Joshi"),
            ("Anita", "Nepal"),
            ("Suman", "Pandey"),
            ("Rekha", "Shah"),
            ("Pratik", "Ghimire"),
            ("Laxmi", "Acharya"),
            ("Binod", "Rana"),
            ("Kriti", "Poudel"),
        ]

        # ----------------------------
        # CREATE USERS
        # ----------------------------
        doctors = []
        patients = []

        # 30 doctors
        for i, (first, last) in enumerate(doctor_data[:30]):

            user = User.objects.create(
                email=f"{first.lower()}.{last.lower()}@medislot.com",
                username=f"{first.lower()}{i}",
                first_name=first,
                last_name=last,
                phone_number=f"98{i}0000000",
                role=User.DOCTOR,
                is_active=True,
            )
            user.set_password("password123")
            user.save()

            doctors.append(user)

        # 20 patients
        for i, (first, last) in enumerate(patient_data):

            user = User.objects.create(
                email=f"{first.lower()}.{last.lower()}@medislot.com",
                username=f"{first.lower()}{i}",
                first_name=first,
                last_name=last,
                phone_number=f"97{i}0000000",
                role=User.PATIENT,
                is_active=True,
            )
            user.set_password("password123")
            user.save()

            patients.append(user)

        self.stdout.write(self.style.SUCCESS("50 users created (30 doctors + 20 patients)"))

        # ----------------------------
        # CREATE DOCTOR PROFILES
        # ----------------------------
        doctor_profiles = []

        for i, user in enumerate(doctors):

            doctor = DoctorProfile.objects.create(
                user=user,
                department=dept_objs[i % len(dept_objs)],
                experience_years=5 + (i % 15),
                qualifications="MBBS, MD (Nepal Medical Council)",
                consultation_fee=500 + (i * 50),
            )

            doctor_profiles.append(doctor)

        self.stdout.write(self.style.SUCCESS("30 doctor profiles created"))

        # ----------------------------
        # SLOT TEMPLATES (NO SATURDAY)
        # ----------------------------
        days = ["MON", "TUE", "WED", "THU", "FRI", "SUN"]

        for doctor in doctor_profiles:
            for day in days:
                SlotTemplate.objects.create(
                    doctor=doctor,
                    day_of_week=day,
                    start_time="10:00",
                    end_time="16:00",
                    slot_quota=5,
                    is_active=True
                )

        self.stdout.write(self.style.SUCCESS("Slot templates created"))
        self.stdout.write(self.style.SUCCESS("🎉 CLEAN REALISTIC DATA READY"))