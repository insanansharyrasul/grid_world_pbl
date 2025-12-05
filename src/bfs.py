from collections import deque

class BreadthFirstSearch:
    def __init__(self, grid_world):
        self.grid = grid_world
        self.start = grid_world.start
        self.goal = grid_world.goal

    def search(self):
        queue = deque([self.start])

        came_from = {self.start: None}

        cost_so_far = {self.start: 0}

        visited_count = 0
        visited = set()

        print(f"[BFS] Memulai pencarian dari {self.start} ke {self.goal}...")

        while queue:
            current = queue.popleft()

            if current in visited:
                continue
            visited.add(current)
            visited_count += 1

            if current == self.goal:
                total_cost = cost_so_far[current]
                print(f"[BFS] Target dicapai! Total Cost: {total_cost}")
                path = self._reconstruct_path(came_from, current)
                return path, total_cost, visited_count

            for neighbor in self.grid.get_neighbors(current):
                if neighbor not in came_from:  
                    movement_cost = self.grid.get_cost(current, neighbor)

                    cost_so_far[neighbor] = cost_so_far[current] + movement_cost
                    came_from[neighbor] = current
                    queue.append(neighbor)

        print("[BFS] Gagal! Tidak ada jalur ditemukan.")
        return None, 0, visited_count

    def _reconstruct_path(self, came_from, current):
        path = []
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        return path[::-1]
