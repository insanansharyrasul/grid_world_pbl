import heapq
import math

class AStar:
    def __init__(self, grid_world, heuristic_type='manhattan'):
        self.grid = grid_world
        self.start = grid_world.start
        self.goal = grid_world.goal
        self.heuristic_type = heuristic_type

    def heuristic(self, a, b):
        x1, y1 = a
        x2, y2 = b
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)

        if self.heuristic_type == 'manhattan':
            return dx + dy
        elif self.heuristic_type == 'euclidean':
            return math.sqrt(dx**2 + dy**2)
        elif self.heuristic_type == 'chebyshev':
            return max(dx, dy)
        else:
            return 0

    def search(self):
        open_set = []
        heapq.heappush(open_set, (0, 0, self.start))
        
        came_from = {self.start: None}
        
        g_score = {self.start: 0}
        
        visited_nodes = set()
        
        visited_count = 0

        while open_set:
            current_f, current_g, current = heapq.heappop(open_set)

            if current in visited_nodes:
                continue

            visited_nodes.add(current)
            visited_count += 1

            if current == self.goal:
                path = self._reconstruct_path(came_from, current)
                return path, g_score[self.goal], visited_count

            neighbors = self.grid.get_neighbors(current)
            for neighbor in neighbors:
                movement_cost = self.grid.get_cost(current, neighbor)
                
                tentative_g = g_score[current] + movement_cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    h = self.heuristic(neighbor, self.goal)
                    f = tentative_g + h
                    
                    heapq.heappush(open_set, (f, tentative_g, neighbor))
                    came_from[neighbor] = current

        return None, 0, visited_count

    def _reconstruct_path(self, came_from, current):
        path = []
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        return path[::-1]