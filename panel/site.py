from django.shortcuts import render, redirect
from dashboard.models import Ust_kategori, Alt_kategori , Site_ayar, Slider
from django.core import serializers
from django.http import JsonResponse, HttpResponseRedirect , HttpResponse
from django.contrib import messages
def ayar(request):
    if request.method == "POST":
        whatsapp = request.POST.get('whatsapp')
        site_title = request.POST.get('site_title')
        site_logo = request.POST.get('site_logo')
        footer_text = request.POST.get('footer_text')
        site_adres = request.POST.get('site_adres')
        site_telefon = request.POST.get('site_telefon')
        site_email = request.POST.get('site_email')
        hakkimizda_text = request.POST.get('hakkimizda_text')
        hakkimizda_baslik = request.POST.get('hakkimizda_baslik')
        text_1 = request.POST.get('text_1')
        text_1_baslik = request.POST.get('text_1_baslik')
        sol_slider = request.POST.get('resim_sol_baslik')
        sag_slider = request.POST.get('resim_sag_baslik')
        hakkimizda_resim_input = request.POST.get('hakkimizda_resim_input')
        ana_sayfa_resim = request.POST.get('ana_sayfa_resim')
        kayit = Site_ayar.objects.get(id = 1)    
        kayit.title=site_title
        if hakkimizda_resim_input:
            kayit.hakkimizda_resim = hakkimizda_resim_input
        
        if ana_sayfa_resim :
            kayit.anasayfa_resim = ana_sayfa_resim 
        if site_logo : 
            kayit.logo = site_logo

        kayit.footer_text = footer_text 
        kayit.adres = site_adres 
        kayit.telefon = site_telefon
        kayit.email = site_email 
        kayit.hakkimizda = hakkimizda_text
        kayit.hakkimizda_baslik = hakkimizda_baslik 
        kayit.text = text_1 
        kayit.text_baslik = text_1_baslik
        kayit.sag_slider = sag_slider
        kayit.sol_slider = sol_slider
        kayit.whatsapp = whatsapp
        kayit.save()
        
        messages.success(request, "Düzenleme işlemi başarılı.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        site_ayar = Site_ayar.objects.get(id = 1)
        slider = Slider.objects.all()
        return render(request, "yonetim/frontend/ayar.html" , {"site_ayar":site_ayar,"slider":slider})
    
def kategori_ajax(request):
    ust = Ust_kategori.objects.all()
    alt = Alt_kategori.objects.all()
    ust_seri = serializers.serialize('json',ust )
    alt_seri = serializers.serialize('json',alt )
    data = {
        "ust" : ust_seri,
        "alt" : alt_seri
    }
    return JsonResponse(data)

def kategoriyi_sil(request ,id , tip):
        if tip == "ust":
            kategori = Ust_kategori.objects.get(id = id)
            alt_kategoriler = Alt_kategori.objects.filter(upper_category = kategori)
            if alt_kategoriler:
                for i in alt_kategoriler:
                    i.delete()
            kategori.delete()
            messages.success(request, "Silme işlemi başarılı.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        elif tip== "alt":
            kategori = Alt_kategori.objects.get(id = id )
            kategori.delete()
            messages.success(request, "Silme işlemi başarılı.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def kategoriyi_ekle(request):
    if request.method == "POST":
        tip = request.POST.get('tip')
        name = request.POST.get('name')
        id_ = request.POST.get('id')
        if tip == "ust":
            kayit = Ust_kategori(name=name)
            kayit.save()
        elif tip =="alt":
            ust_kategori = Ust_kategori.objects.get(id = id_)
            kayit = Alt_kategori(name = name , upper_category = ust_kategori)
            kayit.save()
        
    else : 
        return render (request , "itele.html")

def slider_ekle(request):
    if request.method == "POST":
        tip = request.POST.get('tip')
        resim = request.POST.get('resim')
        yazi = request.POST.get('yazi')
        if tip == "sag":
            kayit = Slider(tip = tip  , resim = resim)
            kayit.save()
        if tip == "sol":
            kayit = Slider(tip = tip  , resim = resim)
            kayit.save()
        data = {
            "id" : kayit.id
        }
        return JsonResponse(data)
    else : 
        return render (request , "itele.html")

def slider_sil(request , id):
    kayit = Slider.objects.get(id = id)
    kayit.delete()
    messages.success(request, "Silme işlemi başarılı.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def slider_ajax(request):
    kayit = Slider.objects.all()
    serialized_kayit = serializers.serialize('json', kayit)
    return HttpResponse(serialized_kayit)