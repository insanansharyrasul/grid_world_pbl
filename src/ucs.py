import heapq
import sys

class Node:
    def __init__(self, position, g_cost, parent=None):
        self.position = position
        self.g_cost = g_cost
        self.parent = parent

    def __lt__(self, other):
        return self.g_cost < other.g_cost

    def __eq__(self, other):
        return self.position == other.position

    def get_position(self):
        return self.position

    def get_g_cost(self):
        return self.g_cost

class UniformCostSearch:
    def __init__(self, grid_world):
        self.grid = grid_world
        self.start_pos = grid_world.start
        self.goal_pos = grid_world.goal
        
        # Inisialisasi struktur data
        self.open_set = []
        self.closed_set = set()
        
        # Tracking biaya minimal ke setiap koordinat
        self.min_costs = {}
        
        # Variabel statistik kinerja
        self.nodes_visited = 0
        self.final_cost = 0
        
        self._initialize_search()

    def _initialize_search(self):
        start_node = Node(self.start_pos, 0)
        heapq.heappush(self.open_set, start_node)
        self.min_costs[self.start_pos] = 0
        
    def search(self):
        while self.open_set:
            # Ambil node dengan g_cost terendah
            current_node = heapq.heappop(self.open_set)
            current_pos = current_node.get_position()

            # cek apakah tujuan tercapai
            if current_pos == self.goal_pos:
                self.final_cost = current_node.get_g_cost()
                return self._reconstruct_path(current_node), self.final_cost, self.nodes_visited

            # abaikan jika node sudah diproses di closed set
            if current_pos in self.closed_set:
                continue

            # tandai node sebagai visited
            self.closed_set.add(current_pos)
            self.nodes_visited += 1

            # proses ekspansi ke tetangga
            self._expand_neighbors(current_node)

        # return kosong jika tidak ada jalur ditemukan
        return None, 0, self.nodes_visited

    def _reconstruct_path(self, current_node):
        path = []
        # backtracking dari goal ke start pakai parent pointer
        while current_node is not None:
            path.append(current_node.get_position())
            current_node = current_node.parent
        return path[::-1]  # Reverse list spy urutan benar (Start ke Goal)
    
    def _expand_neighbors(self, current_node):
        # ambil koordinat
        current_pos = current_node.get_position()
        
        # list tetangga yg valid (tidak keluar peta & bukan tembok)
        # panggil method dari grid world yang sudah kita update
        neighbors = self.grid.get_neighbors(current_pos)

        for neighbor_pos in neighbors:
            # ambil cost masing masing, membedakan ucs dari bfs
            step_cost = self.grid.get_cost(current_pos, neighbor_pos)
            
            # hitung biaya kumulatif (g_cost) baru dari start ke tetangga ini
            tentative_g_cost = current_node.get_g_cost() + step_cost

            # apakah jalur baru ini lebih efisien/murah?
            if self._is_better_path(neighbor_pos, tentative_g_cost):
                self.min_costs[neighbor_pos] = tentative_g_cost
                
                # Buat objek Node baru untuk tetangga, 
                # parent ke current_node agar jalur bisa backtracking
                new_node = Node(neighbor_pos, tentative_g_cost, parent=current_node)
                
                # Push ke priority queue
                # urutkan g_cost (sifat ucs)
                heapq.heappush(self.open_set, new_node)

    def _is_better_path(self, pos, new_cost):
        # apakah node belum pernah dikunjungi 
        # atau cost baru lebih kecil dari cost lama yang tercatat
        if pos not in self.min_costs:
            return True
        if new_cost < self.min_costs[pos]:
            return True
        return False
    
    def get_visited_count(self):
        return self.nodes_visited

    def get_path_cost(self):
        return self.final_cost

    def reset_search(self):
        # reset state pencarian jika ingin dijalankan ulang
        self.open_set = []
        self.closed_set = set()
        self.min_costs = {}
        self.nodes_visited = 0
        self.final_cost = 0
        self._initialize_search()


# unit testing
if __name__ == "__main__":
    class MockGridWorld:
        def __init__(self):
            self.start = (0, 0)
            self.goal = (4, 4)
            self.rows = 5
            self.cols = 5
            self.grid_layout = [
                ['S', '.', '.', '#', '.'],
                ['.', '#', '.', '#', '.'],
                ['.', '#', '.', '.', '.'],
                ['.', '.', '#', '#', '.'],
                ['.', '.', '.', '.', 'G']
            ]
        
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
            return 1

    print("\n--- [UNIT TEST] Running Uniform Cost Search (Standalone) ---")
    
    # Mock Environment
    mock_env = MockGridWorld()
    
    # Solver
    ucs_solver = UniformCostSearch(mock_env)
    
    # Pencarian
    path, cost, visited = ucs_solver.search()
    
    # Hasil
    if path:
        print(f"Status       : SUCCESS")
        print(f"Total Cost   : {cost}")
        print(f"Nodes Visited: {visited}")
        print(f"Path Found   : {path}")
        

        print(f"Start Node   : {path[0] == mock_env.start}")
        print(f"Goal Node    : {path[-1] == mock_env.goal}")
    else:
        print("Status       : FAILED (No Path Found)")
        
    print("--- [UNIT TEST] Completed ---\n")