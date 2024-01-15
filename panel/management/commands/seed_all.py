from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Runs all seed commands'

    def handle(self, *args, **kwargs):
        call_command('seed_site_ayar')
        call_command('seed_popup')
        call_command('seed_blog')
        self.stdout.write(self.style.SUCCESS('Successfully seeded all data!'))