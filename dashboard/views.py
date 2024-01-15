from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Kategori
from django.shortcuts import render, get_object_or_404
from .models import Ust_kategori, Alt_kategori , Site_ayar,Slider , Bize_ulasin
from panel.models import Testler , Sonuclar_alanlar , Alanlar , Analiz_yayin, Sonuclar , Cekilis , Cekilis_alanlar , Popup
from django.http import JsonResponse , HttpResponseRedirect
from django.contrib import messages
from django.forms.models import model_to_dict
def index(request):
    site_ayar = Site_ayar.objects.get(id = 1)
    ust = Ust_kategori.objects.all()
    alt = Alt_kategori.objects.all()
    slider = Slider.objects.all()
    popup = Popup.objects.get(id = 1)
    return render(request , "frontend/dashboard/index.html" , {"site_ayar":site_ayar,"ust":ust , "alt" : alt , "slider":slider , "popup" : popup})


def kategori_listesi(request):
    ana_kategoriler = Kategori.objects.all()
    return render(request, 'kategori_listesi.html', {'ana_kategoriler': ana_kategoriler})

def deneme(request):
    return render(request , "itele.html")


def ust_kategori_view(request, ust_kategori_slug):
    ust_kategori = get_object_or_404(Ust_kategori, slug=ust_kategori_slug)
    alt_kategoriler = Alt_kategori.objects.filter(upper_category=ust_kategori)
    testler = Testler.objects.filter(ust_kategori=ust_kategori)
    if alt_kategoriler.exists():
        return render(request, 'alt_kategoriler_listesi.html', {'alt_kategoriler': alt_kategoriler, 'ust_kategori': ust_kategori, 'testler': testler})
    else:
        return render(request, 'ust_kategori_icerik.html', {'ust_kategori': ust_kategori, 'testler': testler})
    
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
import json

def alt_kategori_view(request, ust_kategori_slug, alt_kategori_slug):
    alt_kategori = get_object_or_404(Alt_kategori, slug=alt_kategori_slug)

    current_datetime = datetime.now()

    active_tests = []
    inactive_tests = []
    one_cikan_test_id = alt_kategori.one_cikan_test_id
    for test in Testler.objects.filter(alt_kategori=alt_kategori).exclude(id=one_cikan_test_id):
        if test.published == '1':
            options = test.options
            if "activeInterval" in options and options["activeInterval"] and \
            "deactiveInterval" in options and options["deactiveInterval"]:
                try:
                    active_date = datetime.strptime(options["activeInterval"], '%Y-%m-%dT%H:%M')
                    deactive_date = datetime.strptime(options["deactiveInterval"], '%Y-%m-%dT%H:%M')
                    
                    if active_date <= current_datetime <= deactive_date:
                        active_tests.append(test)
                    else:
                        inactive_tests.append(test)
                except ValueError:
                    pass

  
    paginator_active = Paginator(active_tests, 1)
    page_active = request.GET.get('page_active')
    try:
        paginated_active_tests = paginator_active.page(page_active)
    except PageNotAnInteger:
        paginated_active_tests = paginator_active.page(1)
    except EmptyPage:
        paginated_active_tests = paginator_active.page(paginator_active.num_pages)

 
    paginator_inactive = Paginator(inactive_tests, 1)
    page_inactive = request.GET.get('page_inactive')
    try:
        paginated_inactive_tests = paginator_inactive.page(page_inactive)
    except PageNotAnInteger:
        paginated_inactive_tests = paginator_inactive.page(1)
    except EmptyPage:
        paginated_inactive_tests = paginator_inactive.page(paginator_inactive.num_pages)
    tests = Testler.objects.filter(alt_kategori=alt_kategori)
    return render(request, 'frontend/test/index.html', {
        'alt_kategori': alt_kategori,
        'active_tests': paginated_active_tests,
        'inactive_tests': paginated_inactive_tests,
        'tests' : tests,
        'slug' : alt_kategori_slug
    })

   
def sonuc_view(request, ust_kategori_slug, alt_kategori_slug):
    alt_kategori = get_object_or_404(Alt_kategori, slug=alt_kategori_slug)

    
    yayinlanmis_test_ids = Analiz_yayin.objects.values_list('test_id', flat=True).distinct()

    
    testler = Testler.objects.filter(id__in=yayinlanmis_test_ids, alt_kategori=alt_kategori)
    return render(request, 'frontend/test/sonuclanmis_testler.html', {'alt_kategori': alt_kategori, 'testler': testler})




def sonuc(request, test_id):
    test = Testler.objects.get(id=test_id)
    cekilis_mesaji = test.cekilis_mesaji
    yayinlanma_mesaji = test.yayinlanma_mesaji
    display_fields = [entry.alan for entry in Sonuclar_alanlar.objects.filter(test=test)]
    
    field_slugs = {}
    for field in display_fields:
        try:
            slug_obj = Alanlar.objects.get(name=field)
            field_slugs[field] = slug_obj.slug
        except Alanlar.DoesNotExist:
            field_slugs[field] = field

    per_page = request.GET.get('per_page', 5)
    from django.db.models import Case, When, Value, IntegerField , F
    sonuclar = (
    Sonuclar.objects.filter(quiz=test , status="finished")
    .annotate(
        sira=Case(
            When(sequence__isnull=True, then=Value(999999)),  # Buradaki 999999 değeri, sequence olmayanların sonda gelmesini sağlar.
            default=F('sequence'),
            output_field=IntegerField()
        )
    )
    .order_by('sira', '-score', 'duration')
    )

    try :
        analiz_yayin = Analiz_yayin.objects.get(test=test)
    except : 
        analiz_yayin = None
    
    paginator = Paginator(sonuclar, per_page)
    page = request.GET.get('page')

    try:
        sonuclar = paginator.page(page)
    except PageNotAnInteger:
        sonuclar = paginator.page(1)
    except EmptyPage:
        sonuclar = paginator.page(paginator.num_pages)

  
    page_number = sonuclar.number
    items_per_page = paginator.per_page
    first_item_number = (page_number - 1) * items_per_page

    context = {
        'display_fields': display_fields,
        'sonuclar': sonuclar,
        'field_slugs': field_slugs,
        'test_id': test.id,
        'analiz_yayin': analiz_yayin,
        'cekilis_mesaji': cekilis_mesaji,
        'yayinlanma_mesaji': yayinlanma_mesaji,
        'test': test,
        'first_item_number': first_item_number  
    }

    return render(request, "frontend/test/sonuc.html", context) 

def hakkimizda(request):
    return render(request, "frontend/dashboard/hakkimizda.html")

def iletisim(request):
    if request.method == "POST" :
        isim = request.POST.get('isim')
        email = request.POST.get('email')
        mesaj = request.POST.get('mesaj')
        kayit = Bize_ulasin( isim = isim , email = email , mesaj = mesaj) 
        kayit.save()
        messages.success(request, "Mesajınız başarı ile tarafımıza ulaşmıştır.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else : 
        return render(request, "frontend/dashboard/iletisim.html")

def sonuc_siniflar(request):
    return render(request, "frontend/test/sonuc-siniflar.html")

def cekilis(request, cekilis_id):
    try:
        test = Testler.objects.get(id=cekilis_id)
    except Testler.DoesNotExist:
        mesaj = "Bu teste henüz bir çekiliş yapılmamış..."
        return render(request, "frontend/test/cekilis-sonuc.html", {"error": mesaj})

    try:
        cekilis = Cekilis.objects.get(quiz=test)
    except Cekilis.DoesNotExist:
        if test.cekilis_mesaji:  # Eğer cekilis_mesaji varsa bu mesajı göster
            return render(request, "frontend/test/cekilis-sonuc.html", {"error": test.cekilis_mesaji})
        else:
            return render(request, "frontend/test/cekilis-sonuc.html", {"error": "Çekiliş bulunamadı."})


    cekilis_alan = Cekilis_alanlar.objects.filter(cekilis=cekilis)
    return render(request, "frontend/test/cekilis-sonuc.html", {"cekilis": cekilis, "cekilis_alan": cekilis_alan , "cekilis_mesaji" : test.cekilis_mesaji})

def test_to_dict(test):
    return {
        'id': test.id,
        'author_id': test.author_id,
        'post_id': test.post_id,
        'title': test.title,
        'description': test.description,
        'quiz_image': test.quiz_image,
        'quiz_category_id': test.quiz_category.id if test.quiz_category else None,
        'question_ids': test.question_ids,
        'ordering': test.ordering,
        'published': test.published,
        'create_date': test.create_date.strftime('%Y-%m-%d %H:%M:%S') if test.create_date else None,
        'options': test.options,
        'intervals': test.intervals,
        'quiz_url': test.quiz_url,
        'kullanici_formu': test.kullanici_formu,
        'yanlis_soru': test.yanlis_soru,
        'alanlar': test.alanlar,
        'ust_kategori': [kategori.id for kategori in test.ust_kategori.all()],
        'alt_kategori': [kategori.id for kategori in test.alt_kategori.all()],
        'yayinlanma_mesaji': test.yayinlanma_mesaji,
        'cekilis_mesaji': test.cekilis_mesaji,
        'tema' : test.tema,
    }

def ajaxx(request , alt_kategori_slug_2):
    if request.method != "POST":
        return JsonResponse({"error": "POST isteği bekleniyor."}, status=400)
    alt_kategori = Alt_kategori.objects.get(slug=alt_kategori_slug_2)
    current_datetime = datetime.now()
    active_tests = []
    inactive_tests = []
    pending_tests = []
    one_cikan_test_id = alt_kategori.one_cikan_test_id


    for test in Testler.objects.filter(alt_kategori=alt_kategori).exclude(id=one_cikan_test_id):
        if test.published == '1':
            options = test.options
            if "activeInterval" in options and options["activeInterval"] and \
            "deactiveInterval" in options and options["deactiveInterval"]:
                try:
                    active_date = datetime.strptime(options["activeInterval"], '%Y-%m-%dT%H:%M')
                    deactive_date = datetime.strptime(options["deactiveInterval"], '%Y-%m-%dT%H:%M')
                    
                    if active_date <= current_datetime <= deactive_date:
                        active_tests.append(test)
                    elif current_datetime < active_date:
                        pending_tests.append(test)
                    else:
                        inactive_tests.append(test)
                except:
                    pass
    tip = request.POST.get("tip")
    page = request.POST.get('page', 1)

    if tip == "active":
        tests = active_tests
        paginator = Paginator(tests, 1)
        try:
            current_test = paginator.page(page)
        except PageNotAnInteger:
            current_test = paginator.page(1)
        except EmptyPage:
            current_test = paginator.page(paginator.num_pages)
        active_tests_data = [test_to_dict(test) for test in current_test.object_list]
        return JsonResponse({"active": active_tests_data,
                              "has_next": current_test.has_next(),
        "has_previous": current_test.has_previous(),
        "next_page_number": current_test.next_page_number() if current_test.has_next() else None,
        "previous_page_number": current_test.previous_page_number() if current_test.has_previous() else None})  
    if tip == "inactive":
        tests = inactive_tests
        paginator = Paginator(tests, 1)
        try:
            current_test = paginator.page(page)
        except PageNotAnInteger:
            current_test = paginator.page(1)
        except EmptyPage:
            current_test = paginator.page(paginator.num_pages)
        inactive_tests_data = [test_to_dict(test) for test in current_test.object_list]
        return JsonResponse({"inactive":inactive_tests_data,
                              "has_next": current_test.has_next(),
        "has_previous": current_test.has_previous(),
        "next_page_number": current_test.next_page_number() if current_test.has_next() else None,
        "previous_page_number": current_test.previous_page_number() if current_test.has_previous() else None}) 

    if tip == "pending":
        tests = pending_tests
        paginator = Paginator(tests, 1)
        try:
            current_test = paginator.page(page)
        except PageNotAnInteger:
            current_test = paginator.page(1)
        except EmptyPage:
            current_test = paginator.page(paginator.num_pages)
        pending_tests_data = [test_to_dict(test) for test in current_test.object_list]
        return JsonResponse({"pending": pending_tests_data,
                              "has_next": current_test.has_next(),
        "has_previous": current_test.has_previous(),
        "next_page_number": current_test.next_page_number() if current_test.has_next() else None,
        "previous_page_number": current_test.previous_page_number() if current_test.has_previous() else None})
    
    if tip == "all":
        active_paginator = Paginator(active_tests, 1)
        inactive_paginator = Paginator(inactive_tests, 1)
        pending_paginator = Paginator(pending_tests, 1)
        active_test = active_paginator.page(1)
        inactive_test = inactive_paginator.page(1)
        pending_test = pending_paginator.page(1)
        active_tests_data = [test_to_dict(test) for test in active_test.object_list]
        inactive_tests_data = [test_to_dict(test) for test in inactive_test.object_list]
        pending_tests_data = [test_to_dict(test) for test in pending_test.object_list]

        return JsonResponse({
            "active": {
                "tests": active_tests_data,
                "has_next": active_test.has_next(),
                "has_previous": active_test.has_previous(),
                "next_page_number": active_test.next_page_number() if active_test.has_next() else None,
                "previous_page_number": active_test.previous_page_number() if active_test.has_previous() else None
            },
            "inactive": {
                "tests": inactive_tests_data,
                "has_next": inactive_test.has_next(),
                "has_previous": inactive_test.has_previous(),
                "next_page_number": inactive_test.next_page_number() if inactive_test.has_next() else None,
                "previous_page_number": inactive_test.previous_page_number() if inactive_test.has_previous() else None
            },
            "pending": {
                "tests": pending_tests_data,
                "has_next": pending_test.has_next(),
                "has_previous": pending_test.has_previous(),
                "next_page_number": pending_test.next_page_number() if pending_test.has_next() else None,
                "previous_page_number": pending_test.previous_page_number() if pending_test.has_previous() else None
            }
        })

    else:
        return JsonResponse({"error": "Geçerli bir test tipi belirtilmedi."}, status=400)

