# Proje Adı

Bu bölümde projenizin kısa bir tanımını yapın. Projeyi ne amaçla geliştirdiğinizi, genel özelliklerini ve işlevlerini burada özetleyin.

## Kurulum

Bu projenin kurulumu için aşağıdaki adımları takip edin.

### Ön Koşullar

- Python 3.x yüklü bir sistem (Linux/Ubuntu tercih edilir)

### Kurulum Adımları

1. **Proje Dosyalarını Kopyalama:**
   Projeyi bir klasöre kopyalayın.

2. **Sanal Ortam Oluşturma ve Aktifleştirme:**
   Terminalde, projenin kopyalandığı klasöre gidin. Sanal ortamı oluşturun ve aktifleştirin:

   ```bash
   python -m venv env
   # Windows için
   env\Scripts\activate
   # Linux/Ubuntu için
   source env/bin/activate

Gerekli Paketlerin Yüklenmesi:
Gerekli paketleri yüklemek için aşağıdaki komutları kullanın:

bash
Copy code
# Windows için
pip install -r requirements.txt
# Ubuntu için
pip install -r requirements-ubuntu.txt
Veritabanı Ayarları ve Migrasyon:
settings.py dosyasını açın ve veritabanı ayarlarınızı yapın. Ardından migrasyonları uygulayın:

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Veritabanı Seed İşlemi:
Başlangıç verilerini oluşturmak için seed komutunu çalıştırın:

bash
Copy code
python manage.py seed_all
Sunucuyu Başlatma:
Django sunucusunu başlatın ve tarayıcınızda uygulamayı görüntüleyin:

bash
Copy code
python manage.py runserver
# Tarayıcınızda localhost:8000 adresine giderek uygulamayı görüntüleyin.
Admin Erişimi
Varsayılan admin kullanıcı adı: admin
Varsayılan admin şifresi: 123qweQWE
