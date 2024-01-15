from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string

class Site_ayar(models.Model):
    title = models.TextField(null=True, blank=True)
    anasayfa_resim = models.TextField(null=True, blank=True)
    logo = models.TextField(null=True, blank=True)
    footer_text = models.TextField(null=True, blank=True)
    adres = models.TextField(null=True, blank=True)
    telefon = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    hakkimizda = models.TextField(null=True, blank=True)
    hakkimizda_baslik = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    text_baslik = models.TextField(null=True, blank=True)
    hakkimizda_resim = models.TextField(null=True, blank=True)
    whatsapp = models.TextField(null=True, blank=True)
    sol_slider = models.TextField(null=True, blank=True)
    sag_slider = models.TextField(null=True, blank=True)

class Slider(models.Model):
    resim = models.TextField(null=True, blank=True)
    tip = models.TextField(null=True, blank=True)
    

class Kategori(models.Model):
    isim = models.CharField(max_length=200)
    ust_kategori = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='alt_kategoriler')
    def _str_(self):
        return self.isim

class Ust_kategori(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_str = slugify(self.name)
            while Ust_kategori.objects.filter(slug=slug_str).exists():
                slug_str = slugify(self.name) + "-" + get_random_string(5).lower()
            self.slug = slug_str
        super(Ust_kategori, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Alt_kategori(models.Model):
    upper_category = models.ForeignKey(Ust_kategori, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    one_cikan_test = models.ForeignKey('panel.Testler', on_delete=models.SET_NULL, null=True, blank=True, related_name="one_cikan_kategorisi")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_str = slugify(self.name)
            while Alt_kategori.objects.filter(slug=slug_str).exists():
                slug_str = slugify(self.name) + "-" + get_random_string(5).lower()
            self.slug = slug_str
        super(Alt_kategori, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Bize_ulasin(models.Model):
    isim = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    mesaj = models.TextField(null=True, blank=True)
    tarih = models.DateTimeField(null=True, blank=True,auto_now_add=True)