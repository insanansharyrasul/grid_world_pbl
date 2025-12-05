class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'
    BG_MAGENTA = '\033[105m'
    BG_CYAN = '\033[106m'
    BG_WHITE = '\033[107m'
    BG_GRAY = '\033[100m'

class GridWorld:
    def __init__(self, input_data):
        self.grid = []
        self.start = None
        self.goal = None
        self.rows = 0
        self.cols = 0
        
        self.costs = {
            '.': 1,
            '@': 3,
            '&': 15,
            '#': float('inf'),
            'S': 1,
            'G': 1
        }

        self._parse_input(input_data)

    def _parse_input(self, data):
        lines = [line.strip() for line in data.strip().split("\n") if line.strip()]

        start_index = 0

        header_parts = lines[0].split()
        if len(header_parts) == 2 and header_parts[0].isdigit():
            start_index = 1

        raw_grid = lines[start_index:]

        for r, line in enumerate(raw_grid):
            row_chars = line.split()
            if len(row_chars) == 1 and len(row_chars[0]) > 1:
                row_chars = list(row_chars[0])

            row_data = []
            for c, char in enumerate(row_chars):
                row_data.append(char)
                if char == "S":
                    self.start = (r, c)
                elif char == "G":
                    self.goal = (r, c)
            self.grid.append(row_data)

        self.rows = len(self.grid)
        self.cols = len(self.grid[0] if self.rows > 0 else 0)

    def get_neighbors(self, node):
        r, c = node
        neighbors = []
        # Arah pergerakan: Atas, Bawah, Kiri, Kanan (4-Connectivity)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                # Cek apakah obstacle (#)
                # Catatan: Lumpur (&) dan Gembur (@) ADALAH walkable (bisa dilewati)
                if self.grid[nr][nc] != "#":
                    neighbors.append((nr, nc))

        return neighbors

    def get_cost(self, from_node, to_node):
        r, c = to_node
        terrain_type = self.grid[r][c]
        return self.costs.get(terrain_type, 1)

    def visualize(self, path=None, current=None, visited=None, show_stats=False, cost=0, nodes_visited=0):
        import os
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
            
        display_grid = [row[:] for row in self.grid]
        visited_cells = set(visited) if visited else set()
        path_cells = set(path) if path else set()

        print(Colors.CYAN + "=" * 60 + Colors.RESET)
        
        for r, row in enumerate(display_grid):
            colored_row = []
            for c, cell in enumerate(row):
                pos = (r, c)
                
                if current and pos == current:
                    colored_row.append(Colors.BG_YELLOW + Colors.BOLD + " X " + Colors.RESET)
                elif cell == "S":
                    colored_row.append(Colors.BG_GREEN + Colors.BOLD + " S " + Colors.RESET)
                elif cell == "G":
                    colored_row.append(Colors.BG_BLUE + Colors.BOLD + " G " + Colors.RESET)
                elif pos in path_cells:
                    colored_row.append(Colors.GREEN + Colors.BOLD + " * " + Colors.RESET)
                elif cell == "#":
                    colored_row.append(Colors.BG_RED + "   " + Colors.RESET)
                elif cell == "&":
                    if pos in visited_cells:
                        colored_row.append(Colors.BG_MAGENTA + " & " + Colors.RESET)
                    else:
                        colored_row.append(Colors.MAGENTA + " & " + Colors.RESET)
                elif cell == "@":
                    if pos in visited_cells:
                        colored_row.append(Colors.BG_YELLOW + " @ " + Colors.RESET)
                    else:
                        colored_row.append(Colors.YELLOW + " @ " + Colors.RESET)
                elif cell == ".":
                    if pos in visited_cells:
                        colored_row.append(Colors.GRAY + " . " + Colors.RESET)
                    else:
                        colored_row.append(Colors.WHITE + " . " + Colors.RESET)
                else:
                    colored_row.append(f" {cell} ")
            
            print("".join(colored_row))
        
        print(Colors.CYAN + "=" * 60 + Colors.RESET)
        
        if show_stats:
            print(f"{Colors.YELLOW}Current Cost: {Colors.BOLD}{cost}{Colors.RESET}")
            print(f"{Colors.CYAN}Nodes Visited: {Colors.BOLD}{nodes_visited}{Colors.RESET}")
            print(Colors.CYAN + "=" * 60 + Colors.RESET)