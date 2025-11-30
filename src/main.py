from grid_environment import GridWorld
from a_star import AStar

if __name__ == "__main__":
    dataset_str = """
    5 5
    S . . . .
    . # . # .
    . # . # .
    . . . # .
    G . . . .
    """

    grid_world = GridWorld(dataset_str)

    print(f"Ukuran Grid: {grid_world.rows}x{grid_world.cols}")
    print(f"Start: {grid_world.start}")
    print(f"Goal: {grid_world.goal}")

    neighbors_of_start = grid_world.get_neighbors(grid_world.start)
    print(f"Tetangga dari Start {grid_world.start}: {neighbors_of_start}")

    grid_world.visualize()
    
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
