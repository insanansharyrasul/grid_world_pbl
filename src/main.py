from grid_environment import GridWorld
from a_star import AStar
from ucs import UniformCostSearch

import os
import time

def load_dataset(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_path, '..', 'datasets', filename)
    
    try:
        with open(dataset_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File {filename} tidak ditemukan di {dataset_path}")
        return None

def get_dataset_files():
    base_path = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_path, '..', 'datasets')
    
    if not os.path.exists(dataset_dir):
        return []

    files = [f for f in os.listdir(dataset_dir) if f.endswith('.txt') and f != 'README.txt']
    return sorted(files)

def run_experiment(grid_world, heuristic, name):
    print(f"\n--- Running {name} ---")
    start_time = time.perf_counter()
    
    solver = AStar(grid_world, heuristic_type=heuristic)
    path, cost, visited = solver.search()
    
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000

    if path:
        print(f"Status: SUCCESS")
        print(f"Total Cost (Energy): {cost}")
        print(f"Nodes Visited (Memory): {visited}")
        print(f"Time: {execution_time:.4f} ms")
        
    else:
        print("Status: FAILED (No Path)")
    
    return path

if __name__ == "__main__":
    dataset_files = get_dataset_files()

    if not dataset_files:
        print("No dataset files found.")
    else:
        for dataset_file in dataset_files:
            print(f"\n{'='*60}")
            print(f"DATASET: {dataset_file}")
            print('='*60)

            content = load_dataset(dataset_file)
            if not content: continue

            grid_world = GridWorld(content)
            
            print("Peta Awal (Legenda: . = Kering(1), @ = Gembur(3), & = Lumpur(15), # = Tembok)")
            grid_world.visualize()

            path_manhattan = run_experiment(grid_world, 'manhattan', "A* (Manhattan Heuristic)")

            path_euclidean = run_experiment(grid_world, 'euclidean', "A* (Euclidean Heuristic)")
            
            if path_euclidean:
                print("\nVisualisasi Jalur (A* Euclidean):")
                grid_world.visualize(path_euclidean)
                
            print(f"\n--- Running UCS (Uniform Cost Search) ---")
            start_time = time.perf_counter()
            
            ucs_solver = UniformCostSearch(grid_world)
            path_ucs, cost_ucs, visited_ucs = ucs_solver.search()
            
            end_time = time.perf_counter()
            execution_time = (end_time - start_time) * 1000

            if path_ucs:
                print(f"Status: SUCCESS")
                print(f"Total Cost: {cost_ucs}")
                print(f"Nodes Visited: {visited_ucs}")
                print(f"Time: {execution_time:.4f} ms")
                # print("Visualisasi Jalur UCS:")
                # grid_world.visualize(path_ucs)
            else:
                print("Status: FAILED")