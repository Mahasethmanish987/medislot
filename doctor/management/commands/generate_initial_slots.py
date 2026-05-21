from django.core.management.base import BaseCommand
from appointment.tasks import initial_generate_7_days

class Command(BaseCommand):
    help = 'Generate initial 7 days of slots for all doctors'

    def handle(self, *args, **options):
        self.stdout.write("Starting initial slot generation for next 7 days...")
        initial_generate_7_days()
        self.stdout.write(self.style.SUCCESS("Successfully generated slots for the next 7 days."))