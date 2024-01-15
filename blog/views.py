from django.shortcuts import render
from django.http import JsonResponse , HttpResponse
from .models import Yazilar , Kategoriler
from django.core.paginator import Paginator


def home(request):
    return HttpResponse("Blog anasayfa")

def blog(request):
    yazilar = Yazilar.objects.filter(durum=1).order_by('-id')
    paginator = Paginator(yazilar, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    kategoriler = Kategoriler.objects.all()
    return render(request,"frontend/blog/index.html" , {"page_obj" : page_obj , "kategoriler":kategoriler , "yazilar" : yazilar})

def blog_view(request , id):
    yazi = Yazilar.objects.get(id = id)
    yazilar = Yazilar.objects.filter( one_cikan="1").order_by('-id')[:3]
    kategoriler = Kategoriler.objects.all()
    return render(request,"frontend/blog/view.html" , {"yazi" : yazi , "kategoriler":kategoriler , "yazilar" : yazilar})


def kategori_view(request , kategori_id):
    kategori = Kategoriler.objects.get( id = kategori_id)
    yazilar = Yazilar.objects.filter(kategori = kategori)
    yazi = Yazilar.objects.filter( one_cikan="1").order_by('-id')[:3]
    paginator = Paginator(yazilar, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    kategoriler = Kategoriler.objects.all()
    return render(request , "frontend/blog/category.html" , {"page_obj" : page_obj , "kategori" : kategori , "kategoriler" : kategoriler , "yazilar" : yazi })