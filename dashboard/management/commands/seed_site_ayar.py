from django.core.management.base import BaseCommand
from dashboard.models import Site_ayar,Slider,Alt_kategori,Ust_kategori
from panel.models import Medya
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Site ayarlarını seed eder'

    def handle(self, *args, **kwargs):
        Site_ayar.objects.create(
            title="Başlık", 
            anasayfa_resim="resim_url",
            logo="logo_url",
            footer_text="Footer metni",
            adres="Adres bilgisi",
            telefon="123456789",
            email="email@example.com",
            hakkimizda="Hakkımızda metni",
            hakkimizda_baslik="Hakkımızda Başlık",
            text="Ekstra metin",
            text_baslik="Ekstra metin başlığı",
            hakkimizda_resim="hakkimizda_resim_url",
            sag_slider="sag_slider_url",
            sol_slider="sol_slider_url",
            whatsapp="whatsapp_numarası"
        )

        Slider.objects.create(
            resim="/medya_dosyalari/resim.png", 
            tip="sag"
        )

        Slider.objects.create(
            resim="/medya_dosyalari/resim.png", 
            tip="sol"
        )

        Ust_kategori.objects.create(
            name="İlkokul", 
            slug="ilkokul"
        )

        Ust_kategori.objects.create(
            name="Orta Okul", 
            slug="orta-okul"
        )

        for i in range(4):
            Alt_kategori.objects.create(
                name=str(i) + ". Sınıf", 
                upper_category_id="1",
                slug=str(i) + "-snf"
            )

        for i in range(4):
            Alt_kategori.objects.create(
                name=str(i+4) + ". Sınıf", 
                upper_category_id="2",
                slug=str(i+4) + "-snf"
            )

        Medya.objects.create(
            tur="RESIM", 
            dosya="medya_dosyalari/resim.png"
        )
        Medya.objects.create(
            tur="RESIM", 
            dosya="medya_dosyalari/resim2.png"
        )
        Medya.objects.create(
            tur="RESIM", 
            dosya="medya_dosyalari/logo.png"
        )
        Medya.objects.create(
            tur="RESIM", 
            dosya="medya_dosyalari/anasayfa.png"
        )
        Medya.objects.create(
            tur="RESIM", 
            dosya="medya_dosyalari/2.png"
        )
        Medya.objects.create(
            tur="RESIM", 
            dosya="medya_dosyalari/3.png"
        )
        Medya.objects.create(
            tur="RESIM", 
            dosya="medya_dosyalari/4.png"
        )
        Medya.objects.create(
            tur="RESIM", 
            dosya="medya_dosyalari/5.png"
        )
        Medya.objects.create(
            tur="RESIM", 
            dosya="medya_dosyalari/6.png"
        )
        Medya.objects.create(
            tur="RESIM", 
            dosya="medya_dosyalari/7.png"
        )
        Medya.objects.create(
            tur="RESIM", 
            dosya="medya_dosyalari/8.png"
        )
        


        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='123qweQWE'
            )
            self.stdout.write(self.style.SUCCESS('Süper kullanıcı başarıyla seed edildi!'))
        else:
            self.stdout.write(self.style.WARNING('Süper kullanıcı zaten var.'))
            
        self.stdout.write(self.style.SUCCESS('Başarıyla seed edildi!'))