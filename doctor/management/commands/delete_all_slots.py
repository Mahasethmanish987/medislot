from django.core.management.base import BaseCommand
from appointment.tasks import initial_generate_7_days
from doctor.models import Slot

class Command(BaseCommand):
    help = 'Generate initial 7 days of slots for all doctors'

    def handle(self, *args, **options):
        self.stdout.write("Deleting all existing slots...")
        Slot.objects.all().delete()
        self.stdout.write("Finished deleting all existing slots.")