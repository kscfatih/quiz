from .models import Ust_kategori, Alt_kategori , Site_ayar

def menu_data(request):
    ust = Ust_kategori.objects.all()
    alt = Alt_kategori.objects.all()
    site_ayar = Site_ayar.objects.get(id = 1)

    return {
        'ust': ust,
        'alt': alt,
        'site_ayar':site_ayar,
    }