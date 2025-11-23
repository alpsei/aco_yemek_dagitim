import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import googlemaps
import os
import folium
import polyline 
from streamlit_folium import st_folium
from dotenv import load_dotenv

from data.coordinates import LOCATIONS
from core.ant_algorithm import AntColonyOptimization
from core.haversine import haversine_distance

# .env dosyasını oku
load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Google Maps İstemcisini başlat
gmaps = None
if API_KEY:
    try:
        gmaps = googlemaps.Client(key=API_KEY)
    except Exception as e:
        print(f"API Hatası: {e}")

st.set_page_config(page_title="Konya Yemek Dağıtım", layout="wide")

st.sidebar.header("Ayarlar")
n_ants = st.sidebar.slider("Karınca Sayısı", 10, 100, 30)
n_iterations = st.sidebar.slider("İterasyon Sayısı", 10, 200, 50)
decay = st.sidebar.slider("Buharlaşma Oranı", 0.1, 0.99, 0.5)
alpha = st.sidebar.slider("Alpha", 0.1, 5.0, 1.0)
beta = st.sidebar.slider("Beta", 0.1, 5.0, 2.0)

if API_KEY:
    st.sidebar.success("API Aktif")
else:
    st.sidebar.warning("API Yok")

yurt_isimleri = list(LOCATIONS.keys())
yurt_koordinatlari = list(LOCATIONS.values())

@st.cache_data
def mesafe_matrisi_olustur(coords):
    n = len(coords)
    matrix = np.zeros((n, n))
    
    if gmaps:
        for i in range(n):
            origin = coords[i]
            try:
                response = gmaps.distance_matrix(origins=[origin], destinations=coords, mode="driving")
                rows = response['rows'][0]['elements']
                for j, element in enumerate(rows):
                    if element['status'] == 'OK':
                        dist_km = element['distance']['value'] / 1000.0
                        matrix[i][j] = dist_km
                    else:
                        matrix[i][j] = np.inf
            except Exception:
                for j in range(n):
                     if i != j: matrix[i][j] = haversine_distance(coords[i], coords[j])
                     else: matrix[i][j] = np.inf
    else:
        for i in range(n):
            for j in range(n):
                if i != j: matrix[i][j] = haversine_distance(coords[i], coords[j])
                else: matrix[i][j] = np.inf
    return matrix

if gmaps:
    st.toast("Google Maps verisi çekiliyor")
else:
    st.toast("Kuş uçuşu hesaplanıyor")

dist_matrix = mesafe_matrisi_olustur(yurt_koordinatlari)

def gercek_rota_getir(sirali_koordinatlar):
    if not gmaps:
        return sirali_koordinatlar # API yoksa düz çizgi döndür
        
    try:
        baslangic = sirali_koordinatlar[0]
        bitis = sirali_koordinatlar[-1]
        duraklar = sirali_koordinatlar[1:-1]
        
        directions_result = gmaps.directions(
            origin=baslangic,
            destination=bitis,
            waypoints=duraklar,
            optimize_waypoints=False,
            mode="driving"
        )
        
        # Gelen veriden "overview_polyline" kısmı alınır koordinata çevrilir
        if directions_result:
            encoded_polyline = directions_result[0]['overview_polyline']['points']
            decoded_points = polyline.decode(encoded_polyline)
            return decoded_points
            
    except Exception as e:
        print(f"Rota çizim hatası: {e}")
        
    return sirali_koordinatlar
def harita_ciz(rota_koordinatlari=None, gercek_yol_verisi=None):
    merkez_lat = np.mean([x[0] for x in yurt_koordinatlari])
    merkez_lon = np.mean([x[1] for x in yurt_koordinatlari])
    
    m = folium.Map(location=[merkez_lat, merkez_lon], zoom_start=12)

    # Noktaları Ekle
    for i, (isim, koord) in enumerate(zip(yurt_isimleri, yurt_koordinatlari)):
        renk = "red" if i == 0 else "blue"
        ikon = "home" if i == 0 else "info-sign"
        
        folium.Marker(
            location=koord,
            popup=isim,
            tooltip=isim,
            icon=folium.Icon(color=renk, icon=ikon)
        ).add_to(m)

    # Rota Çizgisi
    if gercek_yol_verisi:
        # Eğer gerçek yol verisi varsa onu çiz
        folium.PolyLine(
            gercek_yol_verisi,
            color="red",
            weight=5,
            opacity=0.8
        ).add_to(m)
    elif rota_koordinatlari:
        folium.PolyLine(
            rota_koordinatlari,
            color="red",
            weight=5,
            opacity=0.8
        ).add_to(m)
        
    return m

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Dağıtım Noktaları Haritası")
    
    if 'harita_rotasi' not in st.session_state:
        st.session_state.harita_rotasi = None
        st.session_state.gercek_yol_verisi = None
        st.session_state.sonuc_metni = ""
        st.session_state.rota_metni = ""
        st.session_state.gecmis_grafigi = None

    # Haritayı Çiz
    harita = harita_ciz(st.session_state.harita_rotasi, st.session_state.gercek_yol_verisi)
    st_folium(harita, width=700, height=500)
    
    if st.session_state.sonuc_metni:
        st.success(st.session_state.sonuc_metni)
    if st.session_state.rota_metni:
        st.info(st.session_state.rota_metni)

with col2:
    st.subheader("Rota Listesi")
    st.dataframe(pd.DataFrame(yurt_isimleri, columns=["Yurt Adı"]), height=400)
    
    if st.session_state.gecmis_grafigi:
        st.subheader("İyileşme Grafiği")
        fig, ax = plt.subplots()
        ax.plot(st.session_state.gecmis_grafigi, color='green')
        ax.set_title("Her İterasyonda Bulunan En İyi Mesafe")
        ax.set_ylabel("Mesafe (km)")
        ax.set_xlabel("İterasyon")
        ax.grid(True)
        st.pyplot(fig)

if st.button("ROTAYI OPTİMİZE ET", type="primary"):
    with st.spinner('Karıncalar en kısa yolu arıyor...'):
    
        aco = AntColonyOptimization(
            dist_matrix, 
            n_ants=n_ants, 
            n_best=int(n_ants/2), 
            n_iterations=n_iterations, 
            decay=decay, 
            alpha=alpha, 
            beta=beta
        )
        
        en_kisa_yol, gecmis = aco.run()
        
        rota_indeksleri = en_kisa_yol[0] 
        toplam_mesafe = en_kisa_yol[1]
        
        sirali_isimler = []
        sirali_koordinatlar = []
        
        for adim in rota_indeksleri:
            yurt_idx = adim[0]
            sirali_isimler.append(yurt_isimleri[yurt_idx])
            sirali_koordinatlar.append(yurt_koordinatlari[yurt_idx])
            
        son_idx = rota_indeksleri[-1][1]
        sirali_isimler.append(yurt_isimleri[son_idx])
        sirali_koordinatlar.append(yurt_koordinatlari[son_idx])
        
        with st.spinner('Google Maps üzerinden yol güzergahı çiziliyor...'):
            gercek_yol = gercek_rota_getir(sirali_koordinatlar)
        
        st.session_state.harita_rotasi = sirali_koordinatlar
        st.session_state.gercek_yol_verisi = gercek_yol # YENİ: Hafızaya at
        st.session_state.sonuc_metni = f"En Kısa Rota Bulundu! Toplam Mesafe: {toplam_mesafe:.2f} km"
        st.session_state.rota_metni = " ➡️ ".join(sirali_isimler)
        st.session_state.gecmis_grafigi = gecmis
        
        st.rerun()