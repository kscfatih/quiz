from django.urls import path,include
from django.views.static import serve
from . import views

app_name = 'dashboard'

urlpatterns = [  
    path('itele', views.deneme, name='itele'),
    path('', views.index, name='home'),
    path('cekilis-sonuc/<int:cekilis_id>/', views.cekilis, name='cekilis-sonuc'),
    path('test-sonuc/<int:test_id>/', views.sonuc, name='test-sonuc'),
    path('<slug:ust_kategori_slug>/', views.ust_kategori_view, name='ust_kategori'),
    path('<slug:ust_kategori_slug>/<slug:alt_kategori_slug>/', views.alt_kategori_view, name='alt_kategori'),
    path('<slug:ust_kategori_slug>/<slug:alt_kategori_slug>/sonuclanmis-testler', views.sonuc_view, name='sonuc_kategori'),
    path('ajaxx/<str:alt_kategori_slug_2>' , views.ajaxx , name='ajaxx'),
    path('hakkimizda', views.hakkimizda, name='hakkimizda'),
    path('iletisim', views.iletisim, name='iletisim'),
    path('sonuc-siniflar', views.sonuc_siniflar, name='sonuc_siniflar'),
    path('cekilis-sonuc', views.cekilis, name='cekilis-sonuc'),
    
    
]