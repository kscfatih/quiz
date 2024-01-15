from django.urls import path,include
from . import views

app_name = 'blog'

urlpatterns = [  
    path('', views.blog, name='blog'),
    path('view/<int:id>', views.blog_view, name='view'),
    path('kategori/<int:kategori_id>' , views.kategori_view , name='kategori'),
]