from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from doctor.models import DoctorProfile, SlotTemplate

User = get_user_model()

DEFAULT_TEMPLATES = [
    # Monday to Friday – morning slots
    ('MON', '09:00', '10:00', 5),
    ('MON', '10:00', '11:00', 5),
    ('MON', '11:00', '12:00', 5),
    ('TUE', '09:00', '10:00', 5),
    ('TUE', '10:00', '11:00', 5),
    ('TUE', '11:00', '12:00', 5),
    ('WED', '09:00', '10:00', 5),
    ('WED', '10:00', '11:00', 5),
    ('WED', '11:00', '12:00', 5),
    ('THU', '09:00', '10:00', 5),
    ('THU', '10:00', '11:00', 5),
    ('THU', '11:00', '12:00', 5),
    ('FRI', '09:00', '10:00', 5),
    ('FRI', '10:00', '11:00', 5),
    ('FRI', '11:00', '12:00', 5),

    # Sunday – same as Saturday (or you can adjust)
    ('SUN', '09:00', '10:00', 5),
    ('SUN', '10:00', '11:00', 5),
    ('SUN', '11:00', '12:00', 5),
    ('SUN', '12:00', '13:00', 5),
]

class Command(BaseCommand):
    help = 'Seed SlotTemplate for all active doctors with default time slots (including Saturday/Sunday)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Delete existing SlotTemplate for doctors before seeding',
        )

    def handle(self, *args, **options):
        clear_existing = options['clear_existing']
        doctors = DoctorProfile.objects.filter(is_active=True)

        if not doctors.exists():
            self.stdout.write(self.style.WARNING("No active doctors found."))
            return

        created_count = 0
        skipped_count = 0

        for doctor in doctors:
            if clear_existing:
                deleted = SlotTemplate.objects.filter(doctor=doctor).delete()
                self.stdout.write(f"Deleted {deleted[0]} templates for Dr. {doctor.user.get_full_name()}")

            for day, start_str, end_str, quota in DEFAULT_TEMPLATES:
                # Avoid duplicates if not clearing
                exists = SlotTemplate.objects.filter(
                    doctor=doctor,
                    day_of_week=day,
                    start_time=start_str,
                    end_time=end_str
                ).exists()

                if not exists:
                    SlotTemplate.objects.create(
                        doctor=doctor,
                        day_of_week=day,
                        start_time=start_str,
                        end_time=end_str,
                        slot_quota=quota,
                        is_active=True
                    )
                    created_count += 1
                else:
                    skipped_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created {created_count} new SlotTemplates, "
            f"skipped {skipped_count} existing."
        ))