import heapq
import sys

class Node:
    """
    Representasi Node untuk algoritma pathfinding.
    Menyimpan posisi, biaya, dan parent untuk rekonstruksi jalur.
    """
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        
        # g_cost: Biaya aktual dari start node ke node ini
        self.g_cost = 0
        
        # total_cost: Nilai prioritas untuk queue (pada UCS, f = g)
        self.total_cost = 0

    # Method untuk membandingkan apakah dua node sama (berdasarkan posisi)
    def __eq__(self, other):
        return self.position == other.position

    # Method untuk sorting otomatis di Priority Queue (berdasarkan cost terendah)
    def __lt__(self, other):
        return self.total_cost < other.total_cost
    
    # Method string representation untuk debugging
    def __repr__(self):
        return f"Node(pos={self.position}, cost={self.total_cost})"

class UniformCostSearch:
    def __init__(self, grid_world):
        # Menyimpan referensi lingkungan grid
        self.grid = grid_world
        
        # Inisialisasi Node Awal (Start)
        self.start_node = Node(None, grid_world.start)
        self.start_node.g_cost = 0
        self.start_node.total_cost = 0
        
        # Inisialisasi Node Tujuan (Goal)
        self.goal_node = Node(None, grid_world.goal)
        
        # Open List: Node yang akan dievaluasi (Priority Queue)
        self.open_list = []
        
        # Closed List: Node yang sudah selesai dievaluasi
        self.closed_list = []
        
        # Variabel untuk tracking statistik
        self.nodes_visited_count = 0
        self.final_path_cost = 0
        
        
    def search(self):
        # Masukkan node awal ke antrian prioritas
        heapq.heappush(self.open_list, self.start_node)
        
        # Set untuk optimasi pencarian (mencegah loop)
        visited_positions = set()

        while len(self.open_list) > 0:
            # Ambil node dengan cost terendah dari priority queue
            current_node = heapq.heappop(self.open_list)
            self.nodes_visited_count += 1

            # Lazy deletion: Jika posisi sudah dikunjungi, skip
            if current_node.position in visited_positions:
                continue
            
            visited_positions.add(current_node.position)
            self.closed_list.append(current_node)

            # Cek apakah sudah sampai di tujuan
            if current_node == self.goal_node:
                self.final_path_cost = current_node.total_cost
                return self._reconstruct_path(current_node), self.final_path_cost, self.nodes_visited_count

            # Ekspansi node ke tetangga-tetangganya
            self._expand_neighbors(current_node, visited_positions)

        # Jika loop selesai tanpa menemukan tujuan
        return None, 0, self.nodes_visited_count

    def _reconstruct_path(self, current_node):
        path = []
        while current_node is not None:
            path.append(current_node.position)
            current_node = current_node.parent
        return path[::-1]
    
    def _expand_neighbors(self, current_node, visited_positions):
        # Ambil daftar koordinat tetangga yang valid (tidak keluar peta/tembok)
        # Memanggil method dari GridWorld
        neighbors = self.grid.get_neighbors(current_node.position)

        for neighbor_pos in neighbors:
            # Optimasi: Jika node sudah ada di Closed Set, lewati agar tidak looping
            if neighbor_pos in visited_positions:
                continue

            # 1. Hitung Step Cost (Biaya Langkah)
            # Ini akan mengambil nilai 1 (Kering), 3 (Gembur), atau 15 (Lumpur)
            step_cost = self.grid.get_cost(current_node.position, neighbor_pos)
            
            # 2. Hitung Cumulative Cost (Biaya Total dari Start)
            new_g_cost = current_node.g_cost + step_cost

            # 3. Buat Objek Node Baru
            # Parent diset ke current_node untuk keperluan backtracking jalur nanti
            new_node = Node(parent=current_node, position=neighbor_pos)
            
            # Set atribut biaya
            new_node.g_cost = new_g_cost
            new_node.total_cost = new_g_cost  # Prinsip UCS: f(n) = g(n)

            # 4. Masukkan ke Priority Queue (Open List)
            # Heapq otomatis mengurutkan berdasarkan total_cost terkecil
            heapq.heappush(self.open_list, new_node)

    def get_visited_nodes(self):
        # Mengembalikan jumlah node yang telah dievaluasi (untuk benchmarking)
        return self.nodes_visited_count

    def get_final_cost(self):
        # Mengembalikan total biaya energi dari jalur yang ditemukan
        return self.final_path_cost
    
# Unit testing
if __name__ == "__main__":
    # Kelas Mock/Tiruan untuk simulasi GridWorld tanpa file eksternal
    class MockGridWorld:
        def __init__(self):
            self.start = (0, 0)
            self.goal = (4, 4)
            self.rows = 5
            self.cols = 5
            # Peta simulasi: . (1), @ (3), & (15), # (Wall)
            self.grid_layout = [
                ['S', '.', '.', '&', '.'],
                ['.', '#', '.', '#', '.'],
                ['.', '#', '@', '.', '.'],
                ['&', '.', '#', '#', '.'],
                ['.', '.', '.', '.', 'G']
            ]
            # Definisi biaya sesuai kesepakatan kelompok
            self.costs = {'.': 1, '@': 3, '&': 15, 'S': 1, 'G': 1, '#': float('inf')}
        
        def get_neighbors(self, node):
            r, c = node
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            valid_neighbors = []
            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.grid_layout[nr][nc] != '#':
                        valid_neighbors.append((nr, nc))
            return valid_neighbors

        def get_cost(self, from_node, to_node):
            r, c = to_node
            terrain = self.grid_layout[r][c]
            return self.costs.get(terrain, 1)

    print("\n--- [DEMO] Menjalankan Uniform Cost Search (Standalone) ---")
    
    # 1. Inisialisasi Environment Dummy
    mock_env = MockGridWorld()
    print("Peta Simulasi (S=Start, G=Goal, &=Lumpur(15), @=Gembur(3), .=Kering(1))")
    for row in mock_env.grid_layout:
        print(" ".join(row))
    
    # 2. Inisialisasi Solver
    ucs_solver = UniformCostSearch(mock_env)
    
    # 3. Eksekusi Pencarian
    path, cost, visited = ucs_solver.search()
    
    # 4. Tampilkan Hasil
    if path:
        print(f"\nStatus       : SUCCESS")
        print(f"Total Energy : {cost}")
        print(f"Nodes Checked: {visited}")
        print(f"Jalur Solusi : {path}")
    else:
        print("\nStatus       : FAILED (Jalur tidak ditemukan)")
        
    print("--- [DEMO] Selesai ---\n")