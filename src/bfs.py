from collections import deque

class BFS:
    def __init__(self, grid_world):
        self.grid = grid_world
        self.start = grid_world.start
        self.goal = grid_world.goal

    def search(self):
        queue = deque()
        queue.append(self.start)

        came_from = {self.start: None}
        visited = set([self.start])
        visited_nodes_count = 0

        while queue:
            current = queue.popleft()
            visited_nodes_count += 1

            if current == self.goal:
                path = self._reconstruct_path(came_from, current)
                cost = len(path) - 1
                return path, cost, visited_nodes_count

            for neighbor in self.grid.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)

        return None, 0, visited_nodes_count

    def _reconstruct_path(self, came_from, current):
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        return path[::-1]
