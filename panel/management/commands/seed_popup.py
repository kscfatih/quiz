from django.core.management.base import BaseCommand
from panel.models import Popup

class Command(BaseCommand):
    help = 'Site ayarlarını seed eder'

    def handle(self, *args, **kwargs):
        Popup.objects.create(
            resim="https://www.quizvar.com/wp-content/uploads/2021/11/cropped-logo-new-quizvar.png",
            durum="0"
        )
        self.stdout.write(self.style.SUCCESS('Başarıyla seed edildi!'))