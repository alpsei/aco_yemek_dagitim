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


## Kurulum ve Çalıştırma