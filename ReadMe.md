## Proje Hakkında
Bu proje, **Karınca Kolonisi Algoritması (Ant Colony Optimization - ACO)** kullanılarak Konya ilindeki 20 farklı KYK yurduna yemek dağıtımı yapan bir firmanın en kısa rotasını bulmayı amaçlar.

Proje, gerçek dünya verileriyle çalışmaktadır. Mesafeler **Google Maps Distance Matrix API** kullanılarak "Sürüş Modu (Driving)" bazında hesaplanmıştır. Görselleştirme için **Streamlit** ve **Folium** kullanılmıştır.

## Özellikler
* **Gerçek Veriler:** Konya'daki gerçek yurt koordinatları ve Google Maps trafik verileri kullanılır.
* **Hibrit Mesafe Hesabı:** Google Maps API anahtarı varsa gerçek sürüş mesafesi, yoksa veya hata alınırsa otomatik olarak **Haversine (Kuş Uçuşu)** formülü devreye girer.
* **İnteraktif Arayüz:** Streamlit üzerinden karınca sayısı, iterasyon, feromon (alpha) ve mesafe (beta) katsayıları anlık olarak değiştirilebilir.
* **Görselleştirme:**
    * Bulunan en kısa rota Google Maps yol verileriyle harita üzerinde çizilir.
    * Algoritmanın iyileşme süreci (Convergence) grafik ile gösterilir.

## Klasör Yapısı
```text
aco_yemek_dagitim/
│
├── main.py                 # Streamlit ana uygulama dosyası
├── requirements.txt        # Gerekli kütüphaneler listesi
├── .env                    # Google Maps API Anahtarı (Gizli Dosya)
├── README.md               # Proje dokümantasyonu
│
├── data/
│   └── coordinates.py      # Konya yurtlarının koordinat verisi
│
└── core/
    ├── ant_algorithm.py    # Karınca Kolonisi Algoritması (NumPy tabanlı)
    └── haversine.py        # Kuş uçuşu mesafe hesaplama modülü
```
## Kurulum ve Çalıştırma
Projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:
## 1. Projeyi İndirin:
```text
git clone https://github.com/alpsei/aco_yemek_dagitim
cd aco_yemek_dagitim
```
## 2. Sanal Ortamı Oluşturun ve Aktif Edin:
```text
Windows için:

python -m venv venv
.\venv\Scripts\activate

Mac/Linux için:

python3 -m venv venv
source venv/bin/activate
```
## 3. Gerekli Kütüphaneleri Yükleyin:
```text
pip install -r requirements.txt
```
## 4. API Anahtarını Ayarlayın: Proje ana dizininde .env adında bir dosya oluşturun ve içine Google Maps API anahtarınızı ekleyin:
```text
GOOGLE_MAPS_API_KEY=SIZIN_ANAHTARINIZ_BURAYA
```
(Not: API Key girilmezse sistem otomatik olarak Kuş Uçuşu modunda çalışır.)

## 5. Uygulamayı Başlatın:
```text
streamlit run main.py
```
## Algoritma Parametreleri
* **Karınca Sayısı:** Her iterasyonda yola çıkan ajan sayısı.
* **İterasyon:** Algoritmanın kaç döngü çalışacağı.
* **Alpha (Feromon):** Karıncaların kokuya verdiği önem (Tecrübe).
* **Beta (Mesafe):** Karıncaların yolun kısalığına verdiği önem (Açgözlülük).
* **Decay (Buharlaşma):** Her tur sonunda feromonların silinme oranı (0.1 - 0.99).

## Kullanılan Teknolojiler
* Python 3.x
* Streamlit: Web Arayüzü
* NumPy: Matris Hesaplamaları
* Google Maps API: Mesafe ve Rota Verisi
* Folium: Harita Görselleştirme
* Matplotlib: Grafik Çizimi

**Uyarı:** Bu proje eğitim amaçlıdır. .env dosyası .gitignore dosyasına eklenerek API anahtarının GitHub'a yüklenmesi engellenmelidir.
