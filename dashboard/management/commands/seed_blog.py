from django.core.management.base import BaseCommand
from blog.models import Kategoriler,Yazilar

class Command(BaseCommand):
    help = 'Site ayarlarını seed eder'

    def handle(self, *args, **kwargs):

        Kategoriler.objects.create(
            title="Genel Kategori",
            description="Genel Kategori",
            published="1"
        )

        Yazilar.objects.create(
            baslik="Yazı Başlığı",
            icerik="Yazı içeriği",
            tarih="2024-01-13 20:45:14.517294",
            user_id="1",
            kategori_id="1",
            durum="1",
            one_cikan="1",
            resim="/medya_dosyalari/resim.png"
        )

        

        self.stdout.write(self.style.SUCCESS('Başarıyla seed edildi!'))