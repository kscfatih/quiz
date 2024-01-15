from django.db import models
from django.core.exceptions import ValidationError
from dashboard.models import Ust_kategori , Alt_kategori

class Image(models.Model):
    image = models.ImageField(upload_to='images/')

class Kategoriler(models.Model):
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    published = models.TextField(null=True, blank=True)
    options = models.TextField(null=True, blank=True)
    author_id = models.TextField(null=True, blank=True)


class Kategoriler_test(models.Model):
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    published = models.TextField(null=True, blank=True)
    options = models.TextField(null=True, blank=True)
    author_id = models.TextField(null=True, blank=True)

class Sorular(models.Model):
    author_id = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Kategoriler, related_name='Kategoriler', on_delete=models.CASCADE, null=True, blank=True)
    question = models.TextField(null=True, blank=True)
    question_title = models.TextField(null=True, blank=True)
    question_image = models.TextField(null=True, blank=True)
    wrong_answer_text = models.TextField(null=True, blank=True)
    right_answer_text = models.TextField(null=True, blank=True)
    question_hint = models.TextField(null=True, blank=True)
    explanation = models.TextField(null=True, blank=True)
    user_explanation = models.TextField(null=True, blank=True)
    type = models.TextField(null=True, blank=True)
    published = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    not_influence_to_score = models.TextField(null=True, blank=True)
    weight = models.TextField(null=True, blank=True)
    options = models.TextField(null=True, blank=True)
    tag_id = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.id

class Cevaplar(models.Model):
    question = models.ForeignKey(Sorular, related_name='cevaplar', on_delete=models.CASCADE, null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    correct = models.TextField(null=True, blank=True)
    ordering = models.TextField(null=True, blank=True)
    weight = models.TextField(null=True, blank=True)
    keyword = models.TextField(null=True, blank=True)
    placeholder = models.TextField(null=True, blank=True)

class Testler(models.Model):
    author_id = models.TextField(null=True, blank=True)
    post_id = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    quiz_image = models.TextField(null=True, blank=True)
    quiz_category = models.ForeignKey(Kategoriler_test, related_name='kategori', on_delete=models.CASCADE, null=True, blank=True)
    question_ids = models.TextField(null=True, blank=True)
    ordering = models.TextField(null=True, blank=True)
    published = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    options = models.JSONField(null=True, blank=True)
    intervals = models.JSONField(null=True, blank=True)
    quiz_url = models.TextField(null=True, blank=True)
    kullanici_formu = models.TextField(null=True, blank=True)
    yanlis_soru = models.TextField(null=True, blank=True)
    alanlar = models.TextField(null=True, blank=True)
    ust_kategori = models.ManyToManyField(Ust_kategori, blank=True )
    alt_kategori = models.ManyToManyField(Alt_kategori, blank=True )
    yayinlanma_mesaji = models.TextField(null=True, blank=True)
    cekilis_mesaji = models.TextField(null=True, blank=True)
    tema = models.TextField(null=True, blank=True)

    
class Medya(models.Model):
    RESIM = 'RESIM'
    MÜZIK = 'MUZIK'
    VIDEO = 'VIDEO'
    TURLER = [
        (RESIM, 'Resim'),
        (MÜZIK, 'Müzik'),
        (VIDEO, 'Video'),
    ]
    tur = models.CharField(
        max_length=6,
        choices=TURLER,
        default=RESIM,
    )
    dosya = models.FileField(upload_to='medya_dosyalari/')

class Alanlar(models.Model):
    name = models.TextField(null=True, blank=True)
    type = models.TextField(null=True, blank=True)
    slug = models.TextField(null=True, blank=True)
    options = models.TextField(null=True, blank=True)
    published = models.TextField(null=True, blank=True)
    attr_options = models.TextField(null=True, blank=True)
    author_id = models.TextField(null=True, blank=True)


class Sonuclar(models.Model):
    fields = models.JSONField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    ip_adress = models.TextField(null=True, blank=True)
    quiz = models.ForeignKey(Testler, related_name='quiz', on_delete=models.CASCADE, null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    dogru = models.TextField(null=True, blank=True)
    yanlis = models.TextField(null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    sequence = models.IntegerField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.pk or self.fields != Sonuclar.objects.get(pk=self.pk).fields:
            if Sonuclar.objects.filter(fields=self.fields).exists():
                raise ValidationError('Aynı fields değerine sahip bir kayıt zaten var.')
        super(Sonuclar, self).save(*args, **kwargs)


class Sonuclar_alanlar(models.Model):
    alan = models.TextField(null=True, blank=True)
    test = models.ForeignKey('panel.Testler', on_delete=models.CASCADE, null=True, blank=True , related_name='quiz_sonuclar_alanlari')
    

class Analiz_yayin(models.Model):
    test = models.ForeignKey('panel.Testler', on_delete=models.CASCADE, null=True, blank=True , related_name='yayin_quiz')
    durum = models.TextField(null=True, blank=True)


class Leaderboard(models.Model):
    fields = models.JSONField(null=True, blank=True)
    score = models.TextField(null=True, blank=True)
    ip_adress = models.TextField(null=True, blank=True)
    quiz = models.ForeignKey(Testler, related_name='quiz_leaderboard', on_delete=models.CASCADE, null=True, blank=True)
    duration = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    dogru = models.TextField(null=True, blank=True)
    yanlis = models.TextField(null=True, blank=True)
    unique_id = models.TextField(null=True, blank=True)


class Sertifika(models.Model):
    isim = models.CharField(max_length=50)
    issue_date = models.DateField(auto_now_add=True)

class Cekilis(models.Model):
    baslik = models.TextField(null=True, blank=True)
    aciklama = models.TextField(null=True, blank=True)
    quiz = models.ForeignKey(Testler, related_name='quiz_cekilis', on_delete=models.CASCADE, null=True, blank=True)
    
class Cekilis_alanlar(models.Model):
    ad_soyad = models.TextField(null=True, blank=True)
    sinif = models.TextField(null=True, blank=True)
    okul = models.TextField(null=True, blank=True)
    urun = models.TextField(null=True, blank=True)
    resim = models.TextField(null=True, blank=True) 
    aciklama = models.TextField(null=True, blank=True) 
    cekilis = models.ForeignKey(Cekilis, on_delete=models.CASCADE , null=True, blank=True)

class Popup(models.Model):
    resim = models.TextField(null=True , blank = True)
    durum = models.TextField(null=True , blank = True)