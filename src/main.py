from grid_environment import GridWorld
from a_star import AStar
from bfs import BFS
import os

def load_dataset(filename):
    """Load dataset from file"""
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'datasets', filename)
    with open(dataset_path, 'r') as f:
        return f.read()

def get_dataset_files():
    """Get all dataset files from datasets folder"""
    dataset_dir = os.path.join(os.path.dirname(__file__), '..', 'datasets')
    if not os.path.exists(dataset_dir):
        return []

    files = [f for f in os.listdir(dataset_dir) if f.endswith('.txt') and f != 'README.txt']
    return sorted(files)

if __name__ == "__main__":

    dataset_files = get_dataset_files()

    if not dataset_files:
        print("No dataset files found in datasets folder.")
    else:
        for dataset_file in dataset_files:
            print(f"\n{'='*60}")
            print(f"Processing: {dataset_file}")
            print('='*60)


            dataset_str = load_dataset(dataset_file)

            grid_world = GridWorld(dataset_str)

            print(f"Ukuran Grid: {grid_world.rows}x{grid_world.cols}")
            print(f"Start: {grid_world.start}")
            print(f"Goal: {grid_world.goal}")

            neighbors_of_start = grid_world.get_neighbors(grid_world.start)
            print(f"Tetangga dari Start {grid_world.start}: {neighbors_of_start}")

            grid_world.visualize()

            bfs_solver = BFS(grid_world)
            bfs_path, bfs_cost, bfs_visited = bfs_solver.search()

            if bfs_path:
                print("\n[HASIL BFS SEARCH]")
                print(f"Total Langkah (Cost): {bfs_cost}")
                print(f"Total Node Dievaluasi: {bfs_visited}")
                print(f"Rute: {bfs_path}")
                
                print("\nVisualisasi:")
                grid_world.visualize(bfs_path)
            else:
                print("\nTujuan tidak dapat dicapai oleh BFS.")                                                     

            solver = AStar(grid_world)
            path, cost, visited = solver.search()

            if path:
                print("\n[HASIL A* SEARCH]")
                print(f"Total Langkah (Cost): {cost}")
                print(f"Total Node Dievaluasi: {visited}")
                print(f"Rute: {path}")

                print("\nVisualisasi:")
                grid_world.visualize(path)
            else:
                print("\nTujuan tidak dapat dicapai.")
