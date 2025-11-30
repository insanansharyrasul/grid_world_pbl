class AStar:
    def __init__(self, grid_world):
        self.grid = grid_world
        self.start = grid_world.start
        self.goal = grid_world.goal

    def heuristic(self, a, b):
        x1, y1 = a
        x2, y2 = b
        dist_x = x1 - x2 if x1 > x2 else x2 - x1
        dist_y = y1 - y2 if y1 > y2 else y2 - y1
        return dist_x + dist_y

    def get_lowest_f_node(self, open_set):
        best_index = 0
        best_f = open_set[0][0]

        for i in range(1, len(open_set)):
            current_item = open_set[i]
            current_f = current_item[0]
            
            if current_f < best_f:
                best_f = current_f
                best_index = i
        
        return open_set.pop(best_index)

    def search(self):
        open_set = [(0, 0, self.start)]
        came_from = {self.start: None}
        g_score = {self.start: 0}
        visited_nodes_count = 0

        while len(open_set) > 0:
            current_f, current_g, current_node = self.get_lowest_f_node(open_set)
            visited_nodes_count += 1

            if current_node == self.goal:
                path = self._reconstruct_path(came_from, current_node)
                return path, current_g, visited_nodes_count

            neighbors = self.grid.get_neighbors(current_node)
            
            for neighbor in neighbors:
                step_cost = self.grid.get_cost() 
                tentative_g = current_g + step_cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    h = self.heuristic(neighbor, self.goal)
                    f = tentative_g + h
                    
                    open_set.append((f, tentative_g, neighbor))
                    came_from[neighbor] = current_node

        return None, 0, visited_nodes_count

    def _reconstruct_path(self, came_from, current):
        path = []
        while current is not None:
            path.append(current)
            current = came_from.get(current) 
        
        return path[::-1]