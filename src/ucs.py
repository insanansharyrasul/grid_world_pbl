import heapq

class UniformCostSearch:
    def __init__(self, grid_world):
        self.grid = grid_world
        self.start = grid_world.start
        self.goal = grid_world.goal

    def search(self):
        open_set = []
        
        heapq.heappush(open_set, (0, self.start))
        
        came_from = {self.start: None}
        
        cost_so_far = {self.start: 0}
        
        visited_count = 0
        
        closed_set = set()

        print(f"[UCS] Memulai pencarian dari {self.start} ke {self.goal}...")

        while open_set:
            current_cost, current_node = heapq.heappop(open_set)

            if current_node in closed_set:
                continue
            
            closed_set.add(current_node)
            visited_count += 1

            if current_node == self.goal:
                print(f"[UCS] Target dicapai! Total Biaya: {current_cost}")
                path = self._reconstruct_path(came_from, current_node)
                return path, current_cost, visited_count

            # Eksplorasi neighbor
            neighbors = self.grid.get_neighbors(current_node)
            
            for neighbor in neighbors:
                movement_cost = self.grid.get_cost(current_node, neighbor)
                new_cost = cost_so_far[current_node] + movement_cost
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current_node
                    
                    heapq.heappush(open_set, (new_cost, neighbor))

        print("[UCS] Gagal! Tidak ada jalur yang ditemukan.")
        return None, 0, visited_count

    def _reconstruct_path(self, came_from, current):
        path = []
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        return path[::-1]