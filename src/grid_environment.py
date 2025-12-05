class GridWorld:
    def __init__(self, input_data):
        self.grid = []
        self.start = None
        self.goal = None
        self.rows = 0
        self.cols = 0
        
        # Definisi Biaya Medan (Terrain Costs)
        # . = Tanah Kering (Ideal) -> Cost 1
        # @ = Tanah Gembur (Sedang) -> Cost 3
        # & = Lumpur (Berat) -> Cost 15
        # # = Obstacle (Tembok) -> Cost Infinity
        # S/G = Start/Goal -> Cost 1 (Asumsi start/goal di tanah kering)
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

        # Cek apakah baris pertama adalah dimensi (misal: "10 10")
        header_parts = lines[0].split()
        if len(header_parts) == 2 and header_parts[0].isdigit():
            start_index = 1

        raw_grid = lines[start_index:]

        for r, line in enumerate(raw_grid):
            # Handle input yang dipisah spasi atau tidak
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
        """
        Mengembalikan tetangga yang valid (tidak keluar peta dan bukan tembok).
        """
        r, c = node
        neighbors = []
        # Arah pergerakan: Atas, Bawah, Kiri, Kanan (4-Connectivity)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Cek batas grid
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                # Cek apakah obstacle (#)
                # Catatan: Lumpur (&) dan Gembur (@) ADALAH walkable (bisa dilewati)
                if self.grid[nr][nc] != "#":
                    neighbors.append((nr, nc))

        return neighbors

    def get_cost(self, from_node, to_node):
        """
        Mengembalikan biaya bergerak ke node tujuan berdasarkan tipe tanahnya.
        """
        r, c = to_node
        terrain_type = self.grid[r][c]
        
        # Ambil cost dari dictionary, default ke 1 jika tidak dikenal
        return self.costs.get(terrain_type, 1)

    def visualize(self, path=None):
        print("-" * 60)
        # Buat copy grid untuk visualisasi
        display_grid = [row[:] for row in self.grid]

        if path:
            for r, c in path:
                if display_grid[r][c] not in ("S", "G"):
                    # Tandai jalur dengan '*'
                    display_grid[r][c] = "*"

        for row in display_grid:
            # Print row dengan spasi antar karakter agar rapi
            print(" ".join(row))

        print("-" * 60)