from django.shortcuts import render, redirect
from blog.models import Kategoriler , Yazilar
from django.core.paginator import Paginator
from django.http import JsonResponse , HttpResponse , HttpResponseRedirect
from django.contrib import messages

def create(request):
    if request.method == "POST":
        baslik = request.POST.get("baslik")
        yazi = request.POST.get("yazi")
        kategori = request.POST.get("blog-kategori")
        kategori_elemani = Kategoriler.objects.get(id = kategori)
        yayinlanma_durumu = request.POST.get("yayinlanma-durumu")
        one_cikan = request.POST.get("one-cikan")
        hakkimizda_resim_input = request.POST.get("hakkimizda_resim_input")
       
        kayit = Yazilar(baslik = baslik , icerik = yazi , kategori = kategori_elemani , user_id = request.user.id , durum =yayinlanma_durumu , one_cikan =one_cikan , resim = hakkimizda_resim_input )
        kayit.save()
        kategoriler = Kategoriler.objects.all()
        return render(request, "yonetim/panel/blog/create.html" , {"kategoriler":kategoriler})
    else:
        kategoriler = Kategoriler.objects.all()

        return render(request, "yonetim/panel/blog/create.html" , {"kategoriler":kategoriler})
    
def yazilar_list(request):
    yazilar_list = Yazilar.objects.all()
    paginator = Paginator(yazilar_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'yonetim/panel/blog/list.html', {'page_obj': page_obj})

def sil(request , blog_id):
    kayit = Yazilar.objects.get(id = blog_id)
    kayit.delete()
    messages.success(request, "Silme işlemi başarılı")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def kategori_sil(request , id):
    kayit = Kategoriler.objects.get(id = id)
    kayit.delete()
    messages.success(request, "Silme işlemi başarılı")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def duzenle(request , blog_id):
    if request.method == "POST":
        baslik = request.POST.get("baslik")
        yazi = request.POST.get("yazi")
        kategori = request.POST.get("blog-kategori")
        kategori_elemani = Kategoriler.objects.get(id = kategori)
        yayinlanma_durumu = request.POST.get("yayinlanma-durumu")
        one_cikan = request.POST.get("one-cikan")
        hakkimizda_resim_input = request.POST.get("hakkimizda_resim_input")
        kayit = Yazilar.objects.get(id = blog_id)
        
        kayit.resim = hakkimizda_resim_input
        kayit.baslik = baslik
        kayit.icerik = yazi
        kayit.kategori = kategori_elemani
        kayit.durum = yayinlanma_durumu
        kayit.one_cikan = one_cikan
        
        kayit.save()
        yazi = Yazilar.objects.get(id = blog_id)
        kategoriler = Kategoriler.objects.all()
        return render(request , "yonetim/panel/blog/create.html" , {"yazi" : yazi , "kategoriler" : kategoriler})
    else :
        yazi = Yazilar.objects.get(id = blog_id)
        kategoriler = Kategoriler.objects.all()
        return render(request , "yonetim/panel/blog/create.html" , {"yazi" : yazi , "kategoriler" : kategoriler})


def blog_kategori_listele(request):
    kategoriler = Kategoriler.objects.all()
    paginator = Paginator(kategoriler,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request , "yonetim/panel/blog/category/list.html" , {'page_obj': page_obj})