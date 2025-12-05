from utils import MinHeap
import time

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
    def __init__(self, grid_world, visualize=False, delay=0.1):
        self.grid = grid_world
        self.start_pos = grid_world.start
        self.goal_pos = grid_world.goal
        self.visualize_mode = visualize
        self.delay = delay
        
        self.open_set = MinHeap()
        self.closed_set = set()
        self.min_costs = {}
        self.nodes_visited = 0
        self.final_cost = 0
        
        self._initialize_search()

    def _initialize_search(self):
        start_node = Node(self.start_pos, 0)
        self.open_set.push(start_node.get_g_cost(), start_node)
        self.min_costs[self.start_pos] = 0
        
    def search(self):
        while not self.open_set.is_empty():
            _, current_node = self.open_set.pop()
            current_pos = current_node.get_position()

            if current_pos in self.closed_set:
                continue

            self.closed_set.add(current_pos)
            self.nodes_visited += 1

            if self.visualize_mode:
                path_so_far = self._reconstruct_path(current_node)
                self.grid.visualize(
                    path=path_so_far,
                    current=current_pos,
                    visited=self.closed_set,
                    show_stats=True,
                    cost=current_node.get_g_cost(),
                    nodes_visited=self.nodes_visited
                )
                time.sleep(self.delay)

            if current_pos == self.goal_pos:
                self.final_cost = current_node.get_g_cost()
                return self._reconstruct_path(current_node), self.final_cost, self.nodes_visited

            self._expand_neighbors(current_node)

        return None, 0, self.nodes_visited

    def _reconstruct_path(self, current_node):
        path = []
        while current_node is not None:
            path.append(current_node.get_position())
            current_node = current_node.parent
        return path[::-1]
    
    def _expand_neighbors(self, current_node):
        current_pos = current_node.get_position()
        neighbors = self.grid.get_neighbors(current_pos)

        for neighbor_pos in neighbors:
            step_cost = self.grid.get_cost(current_pos, neighbor_pos)
            tentative_g_cost = current_node.get_g_cost() + step_cost

            if self._is_better_path(neighbor_pos, tentative_g_cost):
                self.min_costs[neighbor_pos] = tentative_g_cost
                new_node = Node(neighbor_pos, tentative_g_cost, parent=current_node)
                self.open_set.push(tentative_g_cost, new_node)

    def _is_better_path(self, pos, new_cost):
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
        self.open_set = MinHeap()
        self.closed_set = set()
        self.min_costs = {}
        self.nodes_visited = 0
        self.final_cost = 0
        self._initialize_search()