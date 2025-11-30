class GridWorld:
    def __init__(self, input_data):
        self.grid = []
        self.start = None
        self.goal = None
        self.rows = 0
        self.cols = 0

        self._parse_input(input_data)

    def _parse_input(self, data):
        lines = [line.strip() for line in data.strip().split("\n") if line.strip()]

        start_index = 0

        header_parts = lines[0].split()
        if header_parts[0].isdigit():
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
        # Atas, bawah, kiri, kanan
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for (
            dr,
            dc,
        ) in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] != "#":
                    neighbors.append((nr, nc))

        return neighbors

    def get_cost(self):
        return 1

    def visualize(self, path=None):
        print("-" * 60)
        display_grid = [row[:] for row in self.grid]

        if path:
            for r, c in path:
                if display_grid[r][c] not in ("S", "G"):
                    display_grid[r][c] = "*"

        for row in display_grid:
            print(" ".join(row))

        print("-" * 60)
