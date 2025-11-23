import numpy as np

class AntColonyOptimization:
    """
    distances --> şehirler arası mesafe matrisi
    n_ants --> her turda yola çıkacak karınca sayısı
    n_best --> her turda fenomon bırakmasına izin verilen karınca sayısı
    n_iterations --> programın kaç tur döneceği
    decay --> fenomon buharlaşma oranı (0 ile 1 arası)
    alpha --> fenomonun karınca kararındaki etkisi
    beta --> mesafenin karınca kararındaki etkisi
    """
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
    
    def run(self):
        shortest_path = None # o anki iterasyonun en kısa yolu

        # en iyi yolu saklamak için - başlangıçta sonsuz değerlikli
        all_time_shortest_path = ("placeholder", np.inf)

        # grafik çizdirmek için liste
        history = []

        for i in range(self.n_iterations):
            # karıncalar rota oluşturuyor
            all_paths = self.gen_all_paths()

            # karıncaların geçtiği yollara feromon yay
            self.spread_pheronome(all_paths, self.n_best, shortest_path = shortest_path)

            # bu iterasyonun en kısa yolunu bul
            shortest_path = min(all_paths, key=lambda x: x[1])

            # tüm zamanlardakinden daha kısa yol var mı diye kontrol et varsa tüm zamanlara ekle
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            
            # haritadaki kokuları decay oranıyla azalt
            self.pheromone = self.pheromone * self.decay

            # grafiğe ekle
            history.append(all_time_shortest_path[1])

        return all_time_shortest_path, history
    
    def spread_pheronome(self, all_paths, n_best, shortest_path):
        # yolları kısadan uzuna sırala
        sorted_paths = sorted(all_paths, key= lambda x: x[1])

        # sadece en iyi karınca feromon bırakır
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                # yol ne kadar kısaysa bırakılan koku o kadar fazla
                self.pheromone[move] += 1.0 / self.distances[move]
    
    def gen_path_dist(self, path):
        # verilen rotanın toplam mesafesini hesaplar
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele] # 2 şehir arası mesafeyi topla
        return total_dist
    
    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0) # her karınca depodan başlar (0.index)
            # rotayı ve mesafeyi listeye ekle
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths
    
    # tek bir karıncanın tüm şehirleri gezmesini sağlar
    def gen_path(self, start_node):
        path = []
        visited = set() # ziyaret edilen yurtlar listesi
        visited.add(start_node)
        prev = start_node

        # tüm yurtlar gezilene kadar devam et
        for i in range(len(self.distances) - 1):
            # bir sonraki yurdu seç
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)

            # yolu ekle
            path.append((prev, move))
            prev = move # konumu güncelle
            visited.add(move) # gidilen şehri işaretle
        # iterasyon bitti depoya dön    
        path.append((prev, start_node))
        return path
    
    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        # ziyaret edilen şehirlerin kokusunu 0 yap
        pheromone[list(visited)] = 0

        # karınca algoritması seçim formülü
        # 0'a bölme hatası almamak için 0.0001 gibi çok küçük sayıya böldüm
        row = pheromone ** self.alpha * ((1.0 / (dist + 0.0001)) ** self.beta)
        # olasılıkları normalize et
        norm_row = row / row.sum()

        # rulet tekerleği ile seçim
        move = np.random.choice(self.all_inds, 1, p=norm_row)[0]
        return move

