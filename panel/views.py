from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from django.http import JsonResponse , HttpResponseRedirect
from django.views import View
from .models import Sorular, Testler , Sonuclar
from blog.models import Kategoriler , Yazilar
from dashboard.models import Bize_ulasin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
@login_required(login_url='/panel/login')
def index(request):
    bugunun_tarihi = date.today()
    bugunun_tarihi_metin = bugunun_tarihi.strftime('%Y-%m-%d')
    sonuclar_toplam = Sonuclar.objects.filter(create_date__startswith=bugunun_tarihi_metin)
    sonuclar_sayisi = sonuclar_toplam.count()
    sorular = (Sorular.objects.all()).count()
    testler = (Testler.objects.all()).count()
    sonuclar = (Sonuclar.objects.all()).count()
    return render(request,"yonetim/dashboard/index.html" , {"sorular" : sorular , "testler":testler ,"sonuclar":sonuclar,"toplam_sonuc":sonuclar_sayisi})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('panel:home') 
        else:
            
            return render(request, "yonetim/login/index.html", {"error": "Kullanıcı adı veya şifre hatalı."})

    return render(request,"yonetim/login/index.html")


def logout_view(request):
    logout(request)
    return redirect('panel:login')



online_users = {}

class UpdateUserView(View):
    def get(self, request, *args, **kwargs):
        user_id = request.session.session_key
        if user_id is None:
            request.session.save()
            user_id = request.session.session_key
        online_users[user_id] = datetime.now()

        return JsonResponse({'status': 'ok'})

class GetOnlineUsersView(View):
    def get(self, request, *args, **kwargs):
        global online_users  

        expiration_time = datetime.now() - timedelta(minutes=5)
        online_users = {k: v for k, v in online_users.items() if v > expiration_time}

        return JsonResponse({'online_users': len(online_users)})
    

def quiz2(request):
    return render(request, "test/Quiz2/index.html")

def quiz3(request):
    return render(request, "test/Quiz3/index.html")

def quiz4(request):
    return render(request, "test/Quiz4/index.html")


def blog_kategori_ekle(request):
    if request.method == "POST":
        baslik = request.POST.get("baslik")
        tanim = request.POST.get("tanim")
        kayit = Kategoriler(title = baslik , description = tanim , published = 1)
        kayit.save()
        kategoriler = Kategoriler.objects.all()
        paginator = Paginator(kategoriler,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request , "yonetim/panel/blog/category/list.html" , {'page_obj': page_obj})
    else :
        return render(request , "yonetim/panel/blog/category/create.html")
    
def blog_kategori_duzenle(request , category_id):
    if request.method == "POST":
        return None
    else:
        kategori = Kategoriler.objects.get(id = category_id)
        return render(request , "yonetim/panel/blog/category/create.html" , {"kategori" : kategori})
    

def mesajlar(request):
    mesajlar = Bize_ulasin.objects.all().order_by('-id')
    paginator = Paginator(mesajlar, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "yonetim/panel/bildirim/list.html" , {"page_obj" : page_obj})

def mesaj_sil(request , mesaj_id):
    kayit = Bize_ulasin.objects.get(id = mesaj_id)
    kayit.delete()
    messages.success(request, "Başarılı!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))