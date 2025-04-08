from django.core.management.base import BaseCommand
from payment.services import ChingUpServices

class Command(BaseCommand):
    help = "Fetch a fresh access token using the provided authorization code."



    def handle(self, *args, **kwargs):

        try:
            ChingUpServices.integrate_chingup()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))
