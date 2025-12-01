class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._bubble_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        root = self.heap[0]
        last_item = self.heap.pop()
        if self.heap:
            self.heap[0] = last_item
            self._bubble_down(0)
        return root

    def is_not_empty(self):
        return len(self.heap) > 0

    def _bubble_up(self, index):
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index][0] < self.heap[parent_index][0]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._bubble_up(parent_index)

    def _bubble_down(self, index):
        smallest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        if left_child < len(self.heap) and self.heap[left_child][0] < self.heap[smallest][0]:
            smallest = left_child
        if right_child < len(self.heap) and self.heap[right_child][0] < self.heap[smallest][0]:
            smallest = right_child
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._bubble_down(smallest)


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

    def search(self):
        open_set = MinHeap()
        open_set.push((0, 0, self.start))
        came_from = {self.start: None}
        g_score = {self.start: 0}
        visited_nodes_count = 0

        while open_set.is_not_empty():
            current = open_set.pop()
            if current is None:
                break
            current_f, current_g, current_node = current
            if current_g > g_score.get(current_node, float('inf')):
                continue
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
                    open_set.push((f, tentative_g, neighbor))
                    came_from[neighbor] = current_node

        return None, 0, visited_nodes_count

    def _reconstruct_path(self, came_from, current):
        path = []
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        return path[::-1]