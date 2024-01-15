from django.shortcuts import render, redirect , get_object_or_404
from .forms import ImageForm
from .models import Image , Sorular , Alanlar, Cevaplar , Kategoriler ,Kategoriler_test , Medya , Popup
import os 
from django.views import View
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.views.generic import ListView
from .models import Medya
from .forms import MedyaForm , MedyaForm2
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.views.decorators.csrf import csrf_exempt
def alan_sil(request , id):
    alan = Alanlar.objects.get(id = id )
    alan.delete()
    messages.success(request, "Silme işlemi başarılı.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def alan_ekle(request):
    if request.method == "POST":
        isim = request.POST.getlist("isim[]")
        select_data_json = request.POST.get("select_data")
        if select_data_json:
            select_data = json.loads(select_data_json)
            for x in select_data:
                options_string = ';'.join(x['options'])
                kayit = Alanlar(name = x['name'] , type = "select" , published = "1" , author_id=request.user.id , options = options_string  )
                kayit.save()
                idsi = kayit.id
                kayit.slug = "quiz_attr_"+str(idsi)
                kayit.save()
                messages.success(request, "Ekleme işlemi başarılı.")
        for i in isim:
            kayit = Alanlar(name = i , type = "text" , published = "1" , author_id = request.user.id , options="" )
            kayit.save()
            idsi = kayit.id
            kayit.slug = "quiz_attr_"+str(idsi)
            kayit.save()
            messages.success(request, "Ekleme işlemi başarılı.")

        
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        alanlar = Alanlar.objects.all()
        return render(request , "yonetim/panel/alan_ekle.html" , {"alanlar":alanlar})


def medya_ajax(request):

    tur_param = request.GET.get('tur', None)
    
    if not tur_param:
        medya_list = Medya.objects.all()
    else:
        medya_list = Medya.objects.filter(tur=tur_param)

    medya_list = medya_list.order_by('-id')
    limit = request.GET.get('limit', 5)  
    offset = request.GET.get('offset', 0) 

    medya_list = medya_list[int(offset): int(offset) + int(limit)]
    

    data = serializers.serialize('json', medya_list)

    return JsonResponse(data, safe=False)



def medya_listesi(request):
    medya_turu = request.GET.get('tur')

    if medya_turu and medya_turu != "None":
        medya_list = Medya.objects.filter(tur=medya_turu)
    else:
        medya_list = Medya.objects.all()
        medya_turu = None
    medya_list = medya_list.order_by('-id')
    sayfa = request.GET.get('sayfa', 1)  
    paginator = Paginator(medya_list, 16)  

    try:
        medyalar = paginator.page(sayfa)
    except PageNotAnInteger:
        medyalar = paginator.page(1)
    except EmptyPage:
        medyalar = paginator.page(paginator.num_pages)

    context = {
        'medyalar': medyalar,
        'tur': medya_turu
    }

    return render(request, 'yonetim/panel/medya/listele.html', context)

def upload_media(request):
    if request.method == 'POST':
        form = MedyaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Başarıyla yüklendiğinde yönlendirilecek URL
    else:
        form = MedyaForm()

    return render(request, 'yonetim/panel/medya/yukle.html', {'form': form})

def delete_media(request, media_id):
   
    media = get_object_or_404(Medya, id=media_id)

    media.dosya.delete()

    media.delete()

  
    

    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def medya_yukle(request):
    if request.method == 'POST':
        form = MedyaForm2(data=request.POST, files=request.FILES)
        
        if form.is_valid():
            files = request.FILES.getlist('dosya')
            for f in files:
                medya = Medya(dosya=f, tur=form.cleaned_data['tur'])
                medya.save()
            
            return redirect('panel:deneme')

    else:
        form = MedyaForm2()

    
    return render(request, 'yonetim/panel/medya/toplu-medya-yukle.html', {'form': form})


def ajax_medya_listesi(request):
    limit = request.GET.get('limit', 10)  # Varsayılan olarak 10 kayıt getir.
    offset = request.GET.get('offset', 0)  
    
    medyalar = Medya.objects.all()[offset:offset+limit]

    data = [{
        'id': medya.id,
        'dosya_url': medya.dosya.url,
        'tur': medya.tur,
    } for medya in medyalar]

    return JsonResponse(data, safe=False)





def deneme(request):
    return render(request,"yonetim/panel/quiz/deneme.html")

def user_edit(request):
    user = request.user.id
    user_model = User.objects.get(id = user)
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        user_model.first_name = first_name
        user_model.last_name = last_name
        user_model.username = username
        user_model.email = email
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")
        if old_password and new_password1 and new_password2: 
            if not check_password(old_password, request.user.password):
                messages.error(request, 'Eski şifreniz yanlış!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            elif new_password1 != new_password2:
                messages.error(request, 'Yeni şifreler uyuşmuyor!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            else:
                user_model.set_password(new_password1) 
                user_model.save()
                messages.success(request, 'Şifreniz başarıyla değiştirildi! Lütfen tekrar giriş yapınız.')
                update_session_auth_hash(request, user)
                return redirect('panel:login')
        else:    
            user_model.save()
            messages.success(request, "Düzenleme işlemi başarılı.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return render(request,"yonetim/panel/profile.html" , {"user":user_model})



def sorular(request):
    items_per_page = request.GET.get('items_per_page', 10)  # Varsayılan olarak 10
    sorular_list = Sorular.objects.all()
    paginator = Paginator(sorular_list, items_per_page)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    cevaplar = Cevaplar.objects.all()
    question_count = {}
    kategoriler_list = Kategoriler.objects.all()
    # Bu kısımda sadece paginate edilmiş sorular için cevap sayısı hesaplaması yapılır.
    for question in page:
        question_count[question.id] = Cevaplar.objects.filter(question_id=question.id).count()

    return render(request, "yonetim/panel/question/list.html", {
    "sorular": page.object_list,
    "kategoriler": kategoriler_list,    # Bu satırı değiştirdim.
    "page": page, 
    "cevaplar": cevaplar,
    "question_count": question_count,
    'items_per_page': int(items_per_page)
})

def create_question(request):
    if request.method == 'POST':
        answer = request.POST.getlist('answer[]')
        answer_control = request.POST.getlist('answer_control_2[]')
        answer_key = request.POST.getlist('answer_key[]')
        answer_image = request.POST.getlist('answer_image[]')
        editorContent = request.POST.get("editorContent")
        question_category = request.POST.get("question_category")
        kategori = Kategoriler.objects.get(id=question_category)
        response_text = f"""
        
        answer: {answer}
        answer_control: {answer_control}
        answer_key: {answer_key}
        answer_image: {answer_image}
        editorContent: {editorContent}
        question_category: {question_category}
        """

        soru_kayit = Sorular(author_id = 1 , question = editorContent, category = kategori)
        soru_kayit.save()
        if len(answer) == len(answer_control):
            for i, x  in enumerate(answer):
                if len(answer_image[i]) > 1:
                    cevap_kayit = Cevaplar(question = soru_kayit , answer = x ,keyword=None
                                            , correct = answer_control[i] , image = answer_image[i]  )
                    cevap_kayit.save()
                else:
                    cevap_kayit = Cevaplar(question = soru_kayit , answer = x ,keyword=None
                                            , correct = answer_control[i] )
                    cevap_kayit.save()


        messages.success(request, "Soru kayıt işlemi başarılı.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        kategoriler = Kategoriler.objects.all()

        return render(request,"yonetim/panel/question/create.html" , {"kategoriler":kategoriler})


def soru_sil(request , id):
    soru = Sorular.objects.get(id = id )
    cevaplar = Cevaplar.objects.filter(question = soru)
    for i in cevaplar:
        i.delete()
    soru.delete()
    messages.success(request, "Silme işlemi başarılı")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def soru_duzenle(request , id):
    if request.method == "POST":
        sorular = Sorular.objects.get(id=id)
        cevaplar = Cevaplar.objects.filter(question=sorular)
        answer = request.POST.getlist('answer[]')
        answer_control = request.POST.getlist('answer_control_2[]')
        answer_key = request.POST.getlist('answer_key[]')
        answer_image = request.POST.getlist('answer_image[]')
        editorContent = request.POST.get("editorContent")
        question_category = request.POST.get("question_category")
        kategori = Kategoriler.objects.get(id=question_category)
        if editorContent == "":
            
            sorular.category = kategori
            sorular.save()
        else: 
            sorular.question = editorContent
            sorular.category = kategori
            sorular.save()
        cevaplar_list = list(Cevaplar.objects.filter(question=sorular))
        
        if len(answer) > len(cevaplar):
            for i, ans in enumerate(cevaplar_list):
                if len(answer_image[i]) > 1:
                    cevap = cevaplar_list[i]
                    cevap.answer = answer[i]
                    cevap.correct = answer_control[i]
                    cevap.keyword = None
                    cevap.image = answer_image[i]
                    cevap.save()
                else:
                    cevap = cevaplar_list[i]
                    cevap.answer = answer[i]
                    cevap.correct = answer_control[i]
                    cevap.keyword = None
                    cevap.image = None
                    cevap.save()

            for i in range(len(cevaplar_list), len(answer)):
                if len(answer_image[i]) > 1:
                    new_cevap = Cevaplar(question=sorular, image = answer_image[i] , answer=answer[i], correct=answer_control[i] , keyword = None)
                    new_cevap.save()
                else:
                    new_cevap = Cevaplar(question=sorular, answer=answer[i], correct=answer_control[i] , keyword = None , image = None)
                    new_cevap.save()

            
        elif len(answer) == len(cevaplar):
            
            for i, ans in enumerate(answer):
                if len(answer_image[i]) > 1:
                    cevap = cevaplar_list[i]
                    cevap.answer = ans
                    cevap.correct = answer_control[i]
                    cevap.keyword = None
                    cevap.image = answer_image[i]
                    cevap.save()
                else:
                    cevap = cevaplar_list[i]
                    cevap.answer = ans
                    cevap.correct = answer_control[i]
                    cevap.keyword = None
                    cevap.image = None
                    cevap.save()
            
        else:
            for i, ans in enumerate(answer):
                    cevap = cevaplar_list[i]
                    cevap.answer = ans
                    cevap.correct = answer_control[i]
                    cevap.keyword = None
                    cevap.save()

            for i in range(len(answer), len(cevaplar_list)):
                cevaplar_list[i].delete()
        

            
            
        
        

        messages.success(request, "Düzenleme işlemi başarılı.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    else:
        kategoriler = Kategoriler.objects.all()
        soru = Sorular.objects.get(id=id)
        cevap = Cevaplar.objects.filter(question = soru)
        return render(request,"yonetim/panel/question/create.html" , {"soru":soru , "cevap" : cevap , "kategoriler":kategoriler})



def kategori_ekle(request):
    if request.method == "POST":
        baslik = request.POST.get("baslik")
        tanim = request.POST.get("tanim")
       
        kategori_kayit = Kategoriler(title = baslik , description = tanim)
        kategori_kayit.save()
        messages.success(request, "Kategori ekleme başarılı")
        return render(request,"yonetim/panel/category/index.html")
        
        
    else: 
        return render(request,"yonetim/panel/category/index.html")



def test_kategori_sil(request , id):
    kategori = Kategoriler_test.objects.get(id=id)
    kategori.delete()
    messages.success(request, "Silme işlemi başarılı")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def test_kategori_duzenle(request , id):
    if request.method == "POST":
        kategori = Kategoriler_test.objects.get(id=id)
        baslik = request.POST.get("baslik")
        tanim = request.POST.get("tanim")
        kategori.title = baslik
        kategori.description = tanim
        kategori.save()
        return redirect('panel:categories')
    else:
        kategori = Kategoriler_test.objects.get(id=id)
        return render(request,"yonetim/panel/category/index.html" , {"kategori":kategori})

def test_kategori_ekle(request):
    if request.method == "POST":
        baslik = request.POST.get("baslik")
        tanim = request.POST.get("tanim")
        
        
        kategori_kayit = Kategoriler_test(title = baslik , description = tanim)
        kategori_kayit.save()
        messages.success(request, "Kategori ekleme başarılı")
        return render(request,"yonetim/panel/question/category-list.html")
        
    else: 
        return render(request,"yonetim/panel/category/index.html")


def test_kategori_list(request):
    items_per_page = request.GET.get('items_per_page', 10)  
    kategoriler_list = Kategoriler_test.objects.all()
    

    paginator = Paginator(kategoriler_list, items_per_page)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "yonetim/panel/quiz/category-list.html", {'page': page, 'items_per_page': int(items_per_page)})


def kategori_sil(request , id):
    kategori = Kategoriler.objects.get(id=id)
    kategori.delete()
    messages.success(request, "Silme işlemi başarılı")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def kategori_duzenle(request , id):
    if request.method == "POST":
        kategori = Kategoriler.objects.get(id=id)
        baslik = request.POST.get("baslik")
        tanim = request.POST.get("tanim")
        kategori.title = baslik
        kategori.description = tanim
        kategori.save()
        return redirect('panel:categories')
    else:
        kategori = Kategoriler.objects.get(id=id)
        return render(request,"yonetim/panel/category/index.html" , {"kategori":kategori})


def kategori_list(request):
    items_per_page = request.GET.get('items_per_page', 10)  
    kategoriler_list = Kategoriler.objects.all()
    
    paginator = Paginator(kategoriler_list, items_per_page)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "yonetim/panel/question/category-list.html", {'page': page, 'items_per_page': int(items_per_page)})






def image_upload_view2(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('panel:upload')
    else:
        form = ImageForm()
        
    img = Image.objects.all()
    return render(request, 'yonetim/panel/test/image_upload.html', {'form': form, 'img': img})


def image_upload_view(request):
    return render(request, 'yonetim/panel/test/image_upload.html')



def delete_image(request, image_id):
    img = Image.objects.get(id=image_id)
    if img:
        img_path = os.path.join(settings.MEDIA_ROOT, img.image.path)
        os.remove(img_path)
        img.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def fetch_images(request):
    images = Image.objects.all()
    form = ImageForm()
    html = render_to_string('yonetim/panel/test/partial_images.html', {'img': images, 'form': form})
    return JsonResponse({'html': html})

def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def dashboard(request):
    return render(request, "yonetim/dashboard/index.html")

def popup(request):
    if request.method == "POST":
        kontrol = request.POST.get("kontrol")
        resim = request.POST.get("resim")
        kayit = Popup.objects.get(id = 1)
        kayit.durum = kontrol
        kayit.resim = resim
        kayit.save()
        messages.success(request, "Başarılı.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else: 
        kayit = Popup.objects.get(id = 1)
        return render(request , "yonetim/frontend/popup.html" , {"kayit":kayit})

@csrf_exempt
def upload_media2(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

       
        medya = Medya(tur=Medya.RESIM, dosya=uploaded_file)
        medya.save()

        file_url = medya.dosya.url 

        return JsonResponse({
            'success': True,
            'file_path': file_url
        })
    return JsonResponse({'success': False})