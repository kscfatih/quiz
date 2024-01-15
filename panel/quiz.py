from django.shortcuts import render
from .models import Image , Sorular ,Analiz_yayin , Cekilis , Cekilis_alanlar , Cevaplar , Sonuclar_alanlar , Sonuclar, Sertifika, Kategoriler ,Alanlar, Kategoriler_test, Testler
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from django.http import JsonResponse , HttpResponse , HttpResponseRedirect
from html import unescape
import re
from django.contrib import messages
import json
from django.core import serializers
from datetime import datetime
from dashboard.models import Ust_kategori , Alt_kategori
import random
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.http import JsonResponse

def sertifika_olustur(request):
    if request.method == "POST":
        isim = request.POST.get('isim')
        kayit = Sertifika(isim = isim)
        kayit.save()
        data = {
            "url":f"/panel/sertifika_pdf/{kayit.id}"
        }
        return JsonResponse(data)
    else:
        return render(request , "yonetim/panel/sirac.html")


def analiz_sil(request , id):
    eleman = Sonuclar.objects.get(id = id)
    eleman.delete()
    messages.success(request, "Silme işlemi başarılı.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def analiz(request):
    if request.method == "POST":
        return None
    else:
        sonuc = Sonuclar.objects.all()
        idler = set()
        for i in sonuc:
            id = i.quiz_id
            idler.add(id)
        testler = []
        for x in idler:
            test = Testler.objects.get(id=x)
            testler.append(test)
        
        # id'ye göre sıralama
        sorted_testler = sorted(testler, key=lambda x: x.id, reverse=True)

        # Pagination kısmı
        previous_per_page = int(request.GET.get('per_page', 5))
        per_page = int(request.GET.get('per_page', 5))
        page = int(request.GET.get('page', 1))
    
        if 'per_page' in request.GET and previous_per_page != per_page:
            current_record = (page - 1) * previous_per_page + 1
            page = (current_record + per_page - 1) // per_page
    
        paginator = Paginator(sorted_testler, per_page)
    
        try:
            tests = paginator.page(page)
        except PageNotAnInteger:
            tests = paginator.page(1)
        except EmptyPage:
            tests = paginator.page(paginator.num_pages)
        
        return render(request, "yonetim/panel/quiz/analiz-list.html", {"idler": idler, "testler": tests})



import xlwt
from django.http import HttpResponse

def export_users_xls(request , id):
    quiz = Testler.objects.get(id = id)
    sonuclar = Sonuclar.objects.filter(quiz = quiz , status = "finished")
    serialized_sonuclar = serializers.serialize('json', sonuclar)
    sonuclar_list = json.loads(serialized_sonuclar)
    list_ = []
    for i in sonuclar_list:
            alan = i['fields']['fields']
            list_.append(alan)
            date_str = i['fields']['create_date']
            date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            i['fields']['create_date'] = date_obj
    alanlar_list = []
    for x in list_[0].keys():
            alanlar = Alanlar.objects.get(slug = x)
            isim = alanlar.name 
            alanlar_list.append(isim)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="analiz.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Analiz')

    # Sütun başlıkları tanımla
    row_num = 0
    columns = ['Sayı', *alanlar_list, 'Yanlış Sayısı', 'Doğru Sayısı', 'Skor', 'Süre', 'Tarih']

    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    # Veriyi Excel'e yaz
    for sonuc in sonuclar_list:
        row_num += 1
        row = [
            row_num, 
            *list(sonuc['fields']['fields'].values()),
            sonuc['fields']['yanlis'],
            sonuc['fields']['dogru'],
            sonuc['fields']['score'],
            sonuc['fields']['duration'],
            sonuc['fields']['create_date'].strftime('%d %B %Y %H:%M')
        ]
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, cell_value)

    wb.save(response)
    return response





def analiz_yap(request , id):
    if request.method == "POST":
        alan = request.POST.getlist('alan[]')
        test = Testler.objects.get(id =id )
        test_id = request.POST.get('test_id')
        durum2 = request.POST.get('durum')
        if durum2 :
            try : 
                kayittt = Analiz_yayin.objects.get(test = test)
                kayittt.durum = durum2
                kayittt.test = test
                kayittt.save()
            except:
                kayitt = Analiz_yayin ( durum = durum2 , test = test)
                kayitt.save()
        for i in alan:
            try:
                kayit = Sonuclar_alanlar.objects.get( alan = i , test = test)
                kayit.alan = i
                kayit.save()
            except:
                kayit = Sonuclar_alanlar( alan = i , test = test )
                kayit.save()

        sayi_karistir = request.POST.get('sayi_karistir')
        if sayi_karistir:
            
            top_records = list(Sonuclar.objects.filter(quiz=test , status="finished").order_by('-score')[:int(sayi_karistir)])

        
            random.shuffle(top_records)

            
            for index, obj in enumerate(top_records, start=1):
                obj.sequence = index
                obj.save(update_fields=['sequence'])

        
            remaining_records = Sonuclar.objects.filter(quiz=test , status="finished").exclude(pk__in=[obj.pk for obj in top_records])
            for obj in remaining_records:
                obj.sequence = None  
                obj.save(update_fields=['sequence'])


        messages.success(request, "Başarılı!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        test = Testler.objects.get(id =id )
        durum = Sonuclar_alanlar.objects.filter(test = test)
        if durum:
            durum = "Yayınlandı"
        else:
            durum ="Yayınlanmadı"
        quiz = Testler.objects.get(id = id)
        sonuclar = Sonuclar.objects.filter(quiz = quiz , status="finished")
        if not sonuclar.exists():
           
            return render(request , "yonetim/panel/quiz/analiz-test.html" , {"durum": "Sonuç bulunamadı!"})

        serialized_sonuclar = serializers.serialize('json', sonuclar)
        sonuclar_list = json.loads(serialized_sonuclar)
        list_ = []
        for i in sonuclar_list:
            alan = i['fields']['fields']
            list_.append(alan)
            date_str = i['fields']['create_date']
            date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            i['fields']['create_date'] = date_obj
        alanlar_list = []
        for x in list_[0].keys():
            alanlar = Alanlar.objects.get(slug = x)
            isim = alanlar.name 
            alanlar_list.append(isim)


        results_per_page = request.GET.get('results_per_page', 5)
        try:
            results_per_page = int(results_per_page)
        except ValueError:
            results_per_page = 5
        

        for item in sonuclar_list:
            score_value = item['fields'].get('score', 0)
            if isinstance(score_value, str):
                try:
                    item['fields']['score'] = float(score_value)
                except ValueError: 
                    item['fields']['score'] = 0

            duration = item['fields'].get('duration', 0)
            if isinstance(duration, str):
                try:
                    item['fields']['duration'] = int(duration)
                except ValueError:
                    item['fields']['duration'] = 0
        
        
        arama_terimi = request.GET.get('arama_terimi', '')
        if arama_terimi:
            kelimeler = arama_terimi.split()
            sonuclar_list = [x for x in sonuclar_list if all(any(kelime in str(value) for value in x['fields'].values()) for kelime in kelimeler)]

        
        sonuclar_list.sort(key=lambda x: (x['fields']['score'], -x['fields']['duration']), reverse=True)
        paginator = Paginator(sonuclar_list, results_per_page)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        offset = (page_obj.number - 1) * results_per_page
        try :
            analiz_yayin = Analiz_yayin.objects.get ( test = test)
        except : 
            analiz_yayin = ""
        sonuclar_alanlar = Sonuclar_alanlar.objects.filter(test = test)

        return render(request , "yonetim/panel/quiz/analiz-test.html" , {"durum":durum,"page_obj": page_obj, "list":alanlar_list , "test":test, "offset":offset , "id" : id , "analiz_yayin":analiz_yayin , "sonuclar_alanlar":sonuclar_alanlar})


def create(request):
    if request.method == "POST":
        title = request.POST.get('test-baslik')
        quiz_image = request.POST.get('test-resim')
        description = request.POST.get('test-aciklama')
        quiz_category_id = request.POST.get('test-kategori')
        kategori = Kategoriler_test.objects.get(id = quiz_category_id)
        yayin = request.POST.get('yayinlanma-durumu')
        tema = request.POST.get('tema')

        sorular = request.POST.getlist('test-id[]')
        sorular_change = ','.join(sorular)
        interval = request.POST.getlist('interval-post')
        interval_d = json.loads(interval[0])
        timer = request.POST.get('timer')
        timer_text = request.POST.get('timer_text')
        quiz_tackers_message = request.POST.get('quiz_tackers_message')
        pass_score = request.POST.get('pass_score')
        pass_score_message = request.POST.get('pass_score_message')
        activeInterval = request.POST.get('activeInterval')
        deactiveInterval = request.POST.get('deactiveInterval')
        active_date_message = request.POST.get('active_date_message')
        active_date_pre_start_message = request.POST.get('active_date_pre_start_message')
        quiz_message_before_timer = request.POST.get('quiz_message_before_timer')
        after_timer_text = request.POST.get('after_timer_text')
        randomize_answers = request.POST.get('randomize_answers')
        randomize_questions = request.POST.get('randomize_questions')
        make_questions_required = request.POST.get('make_questions_required')
        enable_navigation_bar = request.POST.get('enable_navigation_bar')
        enable_autostart = request.POST.get('enable_autostart')
        rate_form_title = request.POST.get('rate_form_title')
        kullanici_formu = request.POST.get('kullanici_formu')
        yanlis_soru = request.POST.get('yanlis_soru')
        alanlar = request.POST.get('alanlar')
        yayinlanma_mesaji = request.POST.get('yayinlanma_mesaji')
        cekilis_mesaji = request.POST.get('cekilis_mesaji')
        if alanlar:
            alanlar = alanlar
        else : 
            alanlar = "1,3,5"
        enable_certificate = request.POST.get('enable_certificate')
        data = {
                "enable_autostart":enable_autostart,
                "randomize_answers":randomize_answers,
                "randomize_questions":randomize_questions,
                "make_questions_required":make_questions_required,
                "enable_navigation_bar":enable_navigation_bar,
                "timer":timer,
                "timer_text":timer_text,
                "quiz_tackers_message":quiz_tackers_message,
                "pass_score":pass_score,
                "pass_score_message":pass_score_message,
                "activeInterval":activeInterval,
                "deactiveInterval":deactiveInterval,
                "active_date_message":active_date_message,
                "active_date_pre_start_message":active_date_pre_start_message,
                "quiz_message_before_timer":quiz_message_before_timer,
                "after_timer_text":after_timer_text,
                "rate_form_title":rate_form_title,
                "enable_certificate":enable_certificate
                 }
        if yayin == "0":
            published = 0
        else:
            published = 1
        alt_kategori = request.POST.getlist('alt_category')
        ust_kategori = request.POST.getlist('ust_category')
        
        kayit = Testler (title = title,quiz_image=quiz_image , description = description, quiz_category = kategori, published = published, question_ids= sorular_change,intervals=interval_d,options=data , kullanici_formu=kullanici_formu, yanlis_soru=yanlis_soru , alanlar=alanlar , yayinlanma_mesaji = yayinlanma_mesaji ,cekilis_mesaji = cekilis_mesaji,tema = tema)
        kayit.save()

        for alt_kategori_id in alt_kategori:
            if alt_kategori_id:  
                try:
                    eleman = Alt_kategori.objects.get(id=alt_kategori_id) 
                    kayit.alt_kategori.add(eleman)
                except Alt_kategori.DoesNotExist:
                    pass  
                except ValueError: 
                    pass

        for ust_kategori_id in ust_kategori:
            if ust_kategori_id:  
                try:
                    ust_kategori_eleman = Ust_kategori.objects.get(id=ust_kategori_id)
                    kayit.ust_kategori.add(ust_kategori_eleman)  
                    alt_kategoriler_for_ust = Alt_kategori.objects.filter(upper_category_id=ust_kategori_id)
                    for alt_kategori in alt_kategoriler_for_ust:
                        kayit.alt_kategori.add(alt_kategori)
                except Ust_kategori.DoesNotExist:
                    pass 
                except ValueError: 
                    pass

        one_cikan = request.POST.get('one_cikan')
        if one_cikan:
            if one_cikan == "0":  # Öne çıkan değeri 0'sa kontrol edilecek
                try:
                    kayit2 = Alt_kategori.objects.get(one_cikan_test=kayit)
                    kayit2.one_cikan_test = None
                    kayit2.save()
                except Alt_kategori.DoesNotExist:
                    pass
            else:
                kayit2 = Alt_kategori.objects.get(id=one_cikan)
                kayit2.one_cikan_test = kayit
                kayit2.save()
        
            messages.success(request, "Başarılı!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        ust_kategori = Ust_kategori.objects.all()
        alt_kategori = Alt_kategori.objects.all()
        alanlar = Alanlar.objects.all()
        kategoriler = Kategoriler.objects.all()
        kategoriler_test = Kategoriler_test.objects.all()
        
        return render(request,"yonetim/panel/quiz/create.html" , {"kategoriler":kategoriler , 'kategoriler_test': kategoriler_test ,"alanlar":alanlar , "ust_kategori":ust_kategori , "alt_kategori" : alt_kategori})
    


def edit(request , id):
    if request.method == "POST":
        title = request.POST.get('test-baslik')
        quiz_image = request.POST.get('test-resim')
        description = request.POST.get('test-aciklama')
        quiz_category_id = request.POST.get('test-kategori')
        tema = request.POST.get('tema')

        kategori = Kategoriler_test.objects.get(id = quiz_category_id)
        yayin = request.POST.get('yayinlanma-durumu')
        sorular = request.POST.getlist('test-id[]')
        sorular_change = ','.join(sorular)
        interval = request.POST.getlist('interval-post')
        rate_form_title = request.POST.get('rate_form_title')
        timer = request.POST.get('timer')
        timer_text = request.POST.get('timer_text')
        kullanici_formu = request.POST.get('kullanici_formu')
        yanlis_soru = request.POST.get('yanlis_soru')
        quiz_tackers_message = request.POST.get('quiz_tackers_message')
        pass_score = request.POST.get('pass_score')
        pass_score_message = request.POST.get('pass_score_message')
        activeInterval = request.POST.get('activeInterval')
        deactiveInterval = request.POST.get('deactiveInterval')
        active_date_message = request.POST.get('active_date_message')
        active_date_pre_start_message = request.POST.get('active_date_pre_start_message')
        quiz_message_before_timer = request.POST.get('quiz_message_before_timer')
        after_timer_text = request.POST.get('after_timer_text')
        randomize_answers = request.POST.get('randomize_answers')
        randomize_questions = request.POST.get('randomize_questions')
        make_questions_required = request.POST.get('make_questions_required')
        enable_navigation_bar = request.POST.get('enable_navigation_bar')
        enable_autostart = request.POST.get('enable_autostart')
        alanlar = request.POST.get('alanlar')
        enable_certificate = request.POST.get('enable_certificate')
        yayinlanma_mesaji = request.POST.get('yayinlanma_mesaji')
        cekilis_mesaji = request.POST.get('cekilis_mesaji')
        test = Testler.objects.get(id=id)
        test.yayinlanma_mesaji = yayinlanma_mesaji
        test.cekilis_mesaji = cekilis_mesaji
        test.options['make_questions_required'] = make_questions_required
        test.options['enable_navigation_bar'] = enable_navigation_bar
        test.options['enable_autostart'] = enable_autostart
        test.options['enable_certificate'] = enable_certificate
        test.options['randomize_questions'] = randomize_questions
        test.options['randomize_answers'] = randomize_answers
        test.options['after_timer_text'] = after_timer_text
        test.options['quiz_message_before_timer'] = quiz_message_before_timer
        test.options['active_date_pre_start_message'] = active_date_pre_start_message
        test.options['active_date_message'] = active_date_message
        test.options['deactiveInterval'] = deactiveInterval
        test.options['activeInterval'] = activeInterval
        test.options['pass_score_message'] = pass_score_message
        test.options['pass_score'] = pass_score
        test.options['quiz_tackers_message'] = quiz_tackers_message
        test.options['timer_text'] = timer_text
        test.options['timer'] = timer
        test.options['rate_form_title'] = rate_form_title 
        test.title = title
        test.tema = tema
        test.kullanici_formu = kullanici_formu
        test.yanlis_soru = yanlis_soru
        test.question_ids = sorular_change
        test.intervals = json.loads(interval[0])
        test.published = yayin
        test.quiz_category = kategori
        test.description = description
        test.quiz_image = quiz_image
        test.alanlar = alanlar
        test.save()
        alt_kategori_ids = request.POST.getlist('alt_category') or []
        ust_kategori_ids = request.POST.getlist('ust_category') or []

       
        mevcut_ust_kategoriler = set(test.ust_kategori.all().values_list('id', flat=True))
        mevcut_alt_kategoriler = set(test.alt_kategori.all().values_list('id', flat=True))

     
        for alt_kategori_id in alt_kategori_ids:
            if alt_kategori_id:  
                try:
                    eleman = Alt_kategori.objects.get(id=alt_kategori_id)
                    test.alt_kategori.add(eleman)
                except (Alt_kategori.DoesNotExist, ValueError):
                    pass

        # Üst kategorileri ekleme
        for ust_kategori_id in ust_kategori_ids:
            if ust_kategori_id: 
                try:
                    ust_kategori_eleman = Ust_kategori.objects.get(id=ust_kategori_id)
                    test.ust_kategori.add(ust_kategori_eleman)
                    
                    alt_kategoriler_for_ust = Alt_kategori.objects.filter(upper_category_id=ust_kategori_id)
                    for alt_kategori in alt_kategoriler_for_ust:
                        test.alt_kategori.add(alt_kategori)
                except (Ust_kategori.DoesNotExist, ValueError):
                    pass

        # Silinmesi gereken kategorileri tespit edip sil
        for mevcut_ust_kategori_id in mevcut_ust_kategoriler:
            if str(mevcut_ust_kategori_id) not in ust_kategori_ids:
                test.ust_kategori.remove(mevcut_ust_kategori_id)

     
        for mevcut_alt_kategori_id in mevcut_alt_kategoriler:
            if str(mevcut_alt_kategori_id) not in alt_kategori_ids:
                test.alt_kategori.remove(mevcut_alt_kategori_id)

        testim = Testler.objects.get(id=id)
        one_cikan = request.POST.get('one_cikan')

        if one_cikan:
            existing_alt_kategori = Alt_kategori.objects.filter(one_cikan_test=testim).first()
            if existing_alt_kategori:
                existing_alt_kategori.one_cikan_test = None
                existing_alt_kategori.save()

            try:
                alt_kategori = Alt_kategori.objects.get(id=int(one_cikan))
                alt_kategori.one_cikan_test = testim
                alt_kategori.save()
            except Alt_kategori.DoesNotExist:
                pass  
            except ValueError:
                pass


        
        messages.success(request, "Başarılı!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        alanlar = Alanlar.objects.all()
        test = Testler.objects.get(id=id)
        alan = test.alanlar
        cekilis_mesaji = test.cekilis_mesaji
        yayinlanma_mesaji = test.yayinlanma_mesaji
        alanlar_listesi = [int(i.strip()) for i in alan.split(',')]

        kullanici_formu = test.kullanici_formu
        yanlis_soru = test.yanlis_soru
        kategoriler_test = Kategoriler_test.objects.all()
        kategoriler = Kategoriler.objects.all()
        sorular_listesi = []
        interval = [int(i.strip()) for i in test.question_ids.split(",") if i.strip()]
        for i in interval:
            sorular = Sorular.objects.filter(id = i)
            sorular_listesi.extend(sorular)


        ust_kategori = Ust_kategori.objects.all()
        alt_kategori = Alt_kategori.objects.all()

        secili_ust_kategoriler = []
        secili_alt_kategoriler = []
        try:
            secili_test = Testler.objects.get(id=id)
            secili_ust_kategoriler = secili_test.ust_kategori.all()
            secili_alt_kategoriler = secili_test.alt_kategori.all()
        except Testler.DoesNotExist:
            pass


        return render(request,"yonetim/panel/quiz/create.html" ,{"test":test , "kategoriler":kategoriler,"kategoriler_test":kategoriler_test , "test_option":test.options , "test_interval":test.intervals , "sorular":sorular_listesi , "kullanici_formu":kullanici_formu, "yanlis_soru":yanlis_soru , "alanlar":alanlar , "kayitli_alan":alanlar_listesi,
                                                                 "ust_kategori": ust_kategori ,"alt_kategori" : alt_kategori , "secili_ust_kategoriler": secili_ust_kategoriler,
        "secili_alt_kategoriler": secili_alt_kategoriler,
        "yayinlanma_mesaji":yayinlanma_mesaji,
        "cekilis_mesaji":cekilis_mesaji
                                                                 })
    



def deneme(request):
    return render(request, 'yonetim/panel/quiz/deneme.html')




def ajax_testler(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    category_id = request.GET.get('category_id')

    if category_id:
        results = Testler.objects.filter(quiz_category__id=category_id).order_by('-id')
        
    else:
        results = Testler.objects.all().order_by('-id')
        

    if query:
        results = Testler.objects.filter(title__icontains=query).order_by('-id')
        
    paginator = Paginator(results, 7) # Örnek olarak her sayfada 5 sonuç.
    current_page = paginator.get_page(page) 

    data = {
    'results': [
        {
            'id': obj.id, 
            'tema':obj.tema,
            'title': strip_html_tags(obj.title),  # Burada fonksiyonu kullanıyoruz.
            'description': strip_html_tags(obj.description),
            'category': obj.quiz_category.title,
            'create_date' : obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),
            'sorular': len(obj.question_ids.split(",")),
            
        } 
        for obj in current_page
    ],
    'has_next': current_page.has_next(),
    'next_page_number': current_page.next_page_number() if current_page.has_next() else None,
    'has_previous': current_page.has_previous(),
    'previous_page_number': current_page.previous_page_number() if current_page.has_previous() else None,
}
    return JsonResponse(data)

def ajax_search(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    category_id = request.GET.get('category_id')

    if category_id:
        results = Sorular.objects.filter(category__id=category_id).order_by('-id')
        
    else:
        results = Sorular.objects.all().order_by('-id')
        

    if query:
        results = Sorular.objects.filter(question__icontains=query).order_by('-id')
        
    paginator = Paginator(results, 20) 
    current_page = paginator.get_page(page)

    data = {
    'results': [
        {
            'id': obj.id, 
            'question': strip_html_tags(obj.question), 
            'kategori': obj.category.title, 
            'tarih' : obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),
            'cevap': Cevaplar.objects.filter(question=obj).count()
        } 
        for obj in current_page
    ],
    'has_next': current_page.has_next(),
    'next_page_number': current_page.next_page_number() if current_page.has_next() else None,
    'has_previous': current_page.has_previous(),
    'previous_page_number': current_page.previous_page_number() if current_page.has_previous() else None,
}
    return JsonResponse(data)
def strip_html_tags(html):
    return unescape(re.sub(r'<.*?>', '', html))



def ajax_kategori(request, tip):
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    if tip == "soru":
        results_model = Kategoriler
        count_model = Sorular
        count_field = 'category'
    else:
        results_model = Kategoriler_test
        count_model = Testler
        count_field = 'quiz_category'

    if query:
        results = results_model.objects.filter(title__icontains=query)
    else:
        results = results_model.objects.all()

    paginator = Paginator(results, 1)  
    current_page = paginator.get_page(page)

    data = {
        'results': [
            {
                'id': obj.id,
                'title': strip_html_tags(obj.title), 
                'description': obj.description,
                'sayi': count_model.objects.filter(**{count_field: obj}).count()
            }
            for obj in current_page
        ],
        'has_next': current_page.has_next(),
        'next_page_number': current_page.next_page_number() if current_page.has_next() else None,
        'has_previous': current_page.has_previous(),
        'previous_page_number': current_page.previous_page_number() if current_page.has_previous() else None,
    }

    return JsonResponse(data)

def quiz1(request,id):

    return render(request , "test/Quiz1/index.html" , {"id" : id})

def quiz2(request,id):
    
    return render(request , "test/Quiz2/index.html" , {"id" : id})
def quiz3(request,id):
    
    return render(request , "test/Quiz3/index.html" , {"id" : id})

def quiz4(request,id):
    
    return render(request , "test/Quiz4/index.html" , {"id" : id})

def quiz_ajax(request, id):
    test = Testler.objects.get(id = id)
    alan = test.alanlar
    alanlar_listesi = [int(i.strip()) for i in alan.split(',')]
    alanlarin_listesi = []
    for i in alanlar_listesi:
        aksiyon = Alanlar.objects.get(id = i)
        alanlarin_listesi.append(aksiyon)

    kullanici_formu = test.kullanici_formu
    yanlis_soru = test.yanlis_soru
    interval = test.intervals
    sorular = test.question_ids.split(",")
    option = test.options
    published = test.published
    soru_listesi = []
    cevaplar_listesi = []
    for i in sorular:
        soru = Sorular.objects.filter(id = i)
        soru_listesi.extend(soru)
        cevaplar = Cevaplar.objects.filter(question_id = i)
        cevaplar_listesi.extend(cevaplar)
    
    serialized_sorular = serializers.serialize('json', soru_listesi)
    serialized_cevaplar = serializers.serialize('json', cevaplar_listesi)
    serialized_alanlar = serializers.serialize('json', alanlarin_listesi)
    soru_adedi = len(sorular)

    data = {
        "id" : id,
        "sorular":serialized_sorular,
        "cevaplar": serialized_cevaplar,
        "soru_adedi" : soru_adedi,
        "kullanici_formu": kullanici_formu,
        "options": option,
        "intervals":interval,
        "yanlis_soru":yanlis_soru,
        "alanlar":serialized_alanlar,
        "published": published

    }
    return JsonResponse (data)

def quiz_list(request):
    kategoriler = Kategoriler_test.objects.all()
    return render(request, "yonetim/panel/quiz/list.html" , {"kategoriler":kategoriler})

def delete(request , id):
    test = Testler.objects.get(id = id )
    test.delete()
    messages.success(request, "Silme işlemi başarılı")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def sonuclar_on(request , id):
    if request.method =="POST":
        test = Testler.objects.get(id = id)
        alanlar = [int(i) for i in test.alanlar.split(",")]
        alanlar_listesi = []
        for i in alanlar:
            alanmi = Alanlar.objects.get(id = i)
            alansi = alanmi.slug
            alanlar_listesi.append(alansi)
        alanlar_son = alanlar_son = {
    slug_name: request.POST.get(slug_name).upper() if slug_name == "quiz_attr_1" else request.POST.get(slug_name)
    for slug_name in alanlar_listesi
}
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # En sol IP adresini al
        else:
            ip = request.META.get('REMOTE_ADDR')
        existing_kayit = Sonuclar.objects.filter(fields=alanlar_son).first()
        if existing_kayit:
            return JsonResponse({"id": None})
            
        
        kayit = Sonuclar(fields = alanlar_son , quiz = test , ip_adress = ip, status = "started" , score="0" , duration ="0", dogru ="0" , yanlis = "0" )
        kayit.save()
        data = {"id" : kayit.id}
        return JsonResponse(data)
    else:
        return render(request , "yonetim/panel/sirac.html")


def sonuclar(request ):
    if request.method == "POST":
        k_id = request.POST.get('k_id')
        dogru_sayisi = request.POST.get('dogru_sayisi')
        yanlis_sayisi = request.POST.get('yanlis_sayisi')
        score = request.POST.get('skor')
        timer = request.POST.get('timer')
        kayit = Sonuclar.objects.get(id = k_id)
        kayit.dogru = dogru_sayisi
        kayit.yanlis = yanlis_sayisi
        kayit.score = score
        kayit.duration = timer
        kayit.status = "finished"
        kayit.save()


def cekilis_sonuc(request , test_id):
    if request.method == "POST":
        test = Testler.objects.get(id = test_id)
        cekilis_baslik = request.POST.get('cekilis-baslik')
        cekilis_aciklama = request.POST.get('cekilis-aciklama')
        sayi = request.POST.get('sayi')
        ad_soyad_list = request.POST.getlist('ad_soyad')
        sinif_list = request.POST.getlist('sinif')
        okul_list = request.POST.getlist('okul')
        urun_list = request.POST.getlist('urun')
        hakkimizda_resim_input_list = request.POST.getlist('hakkimizda_resim_input')
        aciklama_list = request.POST.getlist('aciklama')
        try:
            kayit = Cekilis.objects.get(quiz=test)
        except : 
                kayit = None
        if kayit : 
            if cekilis_aciklama != None:
                kayit.aciklama = cekilis_aciklama
            if cekilis_baslik != None:
                kayit.baslik = cekilis_baslik
            
            kayit.quiz = test
            kayit.save()
        else : 
            kayit = Cekilis(baslik = cekilis_baslik , aciklama = cekilis_aciklama , quiz = test)
            kayit.save()

        for ad_soyad, sinif, okul, urun, hakkimizda_resim_input, aciklama in zip(ad_soyad_list, sinif_list, okul_list, urun_list, hakkimizda_resim_input_list, aciklama_list):
            kayit_cekilis = Cekilis_alanlar(ad_soyad = ad_soyad , sinif = sinif , okul = okul , urun = urun ,resim  = hakkimizda_resim_input , aciklama = aciklama , cekilis = kayit)
            kayit_cekilis.save()
            

        
        messages.success(request, "Başarılı!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else: 
        test = Testler.objects.get(id = test_id)
        try:
            cekilis = Cekilis.objects.get(quiz = test)
        except:
            cekilis = None

        cekilis_alanlar = Cekilis_alanlar.objects.filter(cekilis = cekilis)
        return render(request , "yonetim/panel/quiz/cekilis-sonuc.html" , {"cekilis" : cekilis ,"cekilis_alanlar" : cekilis_alanlar })
    
def cekilis_alan_sil(request , cekilis_id):
    kayit = Cekilis_alanlar.objects.get(id = cekilis_id)
    kayit.delete()
    messages.success(request, "Silme işlemi başarılı.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def test_kopyala(request , test_id ):
    test = Testler.objects.get(id = test_id)
    test.pk = None
    test.published = 0
    test.save()
    messages.success(request, "Testi kopyalama işlemi başarılı.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def sonuc_gorunlule_panel(request, test_id):
    test = Testler.objects.get(id=test_id)
    
    display_fields = [entry.alan for entry in Sonuclar_alanlar.objects.filter(test=test)]
    
    field_slugs = {}
    for field in display_fields:
        try:
            slug_obj = Alanlar.objects.get(name=field)
            field_slugs[field] = slug_obj.slug
        except Alanlar.DoesNotExist:
            field_slugs[field] = field
    per_page = request.GET.get('per_page', 5)
    from django.db.models import F
    sonuclar = Sonuclar.objects.filter(quiz=test, status="finished").order_by(
    F('sequence').asc(nulls_last=True), '-score', 'duration'
    )
    # Paginator objesi oluştur
    paginator = Paginator(sonuclar, per_page)  # Örnek olarak her sayfada 10 sonuç gösteriliyor
    page = request.GET.get('page')

    try:
        sonuclar = paginator.page(page)
    except PageNotAnInteger:
        sonuclar = paginator.page(1)
    except EmptyPage:
        sonuclar = paginator.page(paginator.num_pages)

    context = {
        'display_fields': display_fields,
        'sonuclar': sonuclar,
        'field_slugs': field_slugs,
        'test_id' : test.id
    }

    return render(request, "yonetim/panel/quiz/karisik-sonuc.html", context)



@csrf_exempt
def sonuc_alani_sil(request , sonuc_id):
    sonuc = Sonuclar_alanlar.objects.get( id = sonuc_id)
    sonuc.delete()
    return HttpResponse("Başarılı")

