import numpy as np

def haversine_distance(coord1, coord2):
    R = 6371.0 # dünyanın km cinsinden yarıçapı

    # bilgisayardaki sin - cos fonksiyonları dereceyle değil radyan ile çalıştığı için 
    # koordinatları radyana dönüştürmek gerekiyor
    lat1, lon1 = np.radians(coord1)
    lat2, lon2 = np.radians(coord2)

    # delta hesabı
    dlat = lat2 - lat2
    dlon = lon2 - lon1

    # küre üzerinde açı hesaplamak için
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2

    # 2 nokta arasındaki açının radyan değerini almak için
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 -a))

    # yarıçap x açı = mesafe
    distance = R * c

    return distance