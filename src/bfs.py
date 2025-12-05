from utils import Queue
import time

class BreadthFirstSearch:
    def __init__(self, grid_world, visualize=False, delay=0.1):
        self.grid = grid_world
        self.start = grid_world.start
        self.goal = grid_world.goal
        self.visualize_mode = visualize
        self.delay = delay

    def search(self):
        queue = Queue()
        queue.push(self.start)

        came_from = {self.start: None}
        cost_so_far = {self.start: 0}
        visited_count = 0
        visited = set()

        print(f"[BFS] Memulai pencarian dari {self.start} ke {self.goal}...")

        while not queue.is_empty():
            current = queue.pop()

            if current in visited:
                continue
            visited.add(current)
            visited_count += 1

            if self.visualize_mode:
                path_so_far = self._reconstruct_path(came_from, current)
                self.grid.visualize(
                    path=path_so_far,
                    current=current,
                    visited=visited,
                    show_stats=True,
                    cost=cost_so_far[current],
                    nodes_visited=visited_count
                )
                time.sleep(self.delay)

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
                    queue.push(neighbor)

        print("[BFS] Gagal! Tidak ada jalur ditemukan.")
        return None, 0, visited_count

    def _reconstruct_path(self, came_from, current):
        path = []
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        return path[::-1]
