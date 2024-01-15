from django.db import models

class Kategoriler(models.Model):
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    published = models.TextField(null=True, blank=True)
    

class Yazilar(models.Model):
    baslik = models.TextField(null=True, blank=True)
    icerik = models.TextField(null=True, blank=True)
    tarih = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    user_id = models.TextField(null=True, blank=True)
    durum = models.TextField(null=True, blank=True)
    resim = models.TextField(null=True, blank=True)
    one_cikan = models.TextField(null=True, blank=True)
    kategori = models.ForeignKey(Kategoriler, related_name='kategoriler', on_delete=models.CASCADE, null=True, blank=True)