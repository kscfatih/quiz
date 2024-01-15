QUİZ PLATFORMU

## Kurulum

Projenin kurulumu için aşağıdaki adımları izleyin:

Proje dosyalarını yerel bir klasöre kopyalayın.

Terminali açın ve projenin kopyalandığı klasörün yoluna gidin.

Sanal ortamı oluşturun: python -m venv env

Sanal ortamı etkinleştirin (Linux için):
source env/bin/activate

Sanal ortamı etkinleştirin (Windows için):
env\Scripts\activate

Gerekli paketleri yükleyin:
pip install -r requirements.txt

Ubuntu için gerekiyorsa:
pip install -r requirements-ubuntu.txt

settings.py dosyasını düzenleyerek veritabanı bilgilerinizi ekleyin.
Veritabanını oluşturmak için aşağıdaki komutları çalıştırın:
python manage.py makemigrations
python manage.py migrate

Seed işlemi için başlangıç verilerini eklemek için aşağıdaki komutu çalıştırın:
python manage.py seed_all

Proje sunucusunu başlatın:
python manage.py runserver
