from grid_environment import GridWorld, Colors
from a_star import AStar
from ucs import UniformCostSearch
from bfs import BreadthFirstSearch

import os
import time

def load_dataset(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_path, '..', 'datasets', filename)
    
    try:
        with open(dataset_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"{Colors.RED}Error: File {filename} tidak ditemukan di {dataset_path}{Colors.RESET}")
        return None

def get_dataset_files():
    base_path = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_path, '..', 'datasets')
    
    if not os.path.exists(dataset_dir):
        return []

    files = [f for f in os.listdir(dataset_dir) if f.endswith('.txt') and f != 'README.txt']
    return sorted(files)

def display_dataset_menu(dataset_files):
    print("\n" + Colors.CYAN + "="*60 + Colors.RESET)
    print(Colors.BOLD + Colors.BLUE + "DAFTAR DATASET TERSEDIA" + Colors.RESET)
    print(Colors.CYAN + "="*60 + Colors.RESET)
    
    for idx, filename in enumerate(dataset_files, 1):
        print(f"  {Colors.GREEN}{idx}.{Colors.RESET} {filename}")
    
    print(f"  {Colors.RED}0.{Colors.RESET} Keluar")
    print(Colors.CYAN + "="*60 + Colors.RESET)

def display_algorithm_menu():
    print("\n" + Colors.CYAN + "="*60 + Colors.RESET)
    print(Colors.BOLD + Colors.BLUE + "PILIH ALGORITMA" + Colors.RESET)
    print(Colors.CYAN + "="*60 + Colors.RESET)
    print(f"  {Colors.GREEN}1.{Colors.RESET} BFS (Breadth-First Search)")
    print(f"  {Colors.GREEN}2.{Colors.RESET} UCS (Uniform Cost Search)")
    print(f"  {Colors.GREEN}3.{Colors.RESET} A* (Manhattan Heuristic)")
    print(f"  {Colors.GREEN}4.{Colors.RESET} A* (Euclidean Heuristic)")
    print(f"  {Colors.GREEN}5.{Colors.RESET} Run All Algorithms (Comparison)")
    print(f"  {Colors.RED}0.{Colors.RESET} Kembali")
    print(Colors.CYAN + "="*60 + Colors.RESET)

def print_comparison_table(results):
    print("\n" + Colors.CYAN + "="*80 + Colors.RESET)
    print(Colors.BOLD + Colors.YELLOW + "TABEL PERBANDINGAN ALGORITMA" + Colors.RESET)
    print(Colors.CYAN + "="*80 + Colors.RESET)
    
    print(f"{Colors.BOLD}{'Algoritma':<25} {'Status':<10} {'Cost':<12} {'Visited':<12} {'Time (ms)':<12}{Colors.RESET}")
    print(Colors.GRAY + "-"*80 + Colors.RESET)
    
    for result in results:
        algo = result['algo']
        status = result['status']
        
        if result['status'] == 'SUCCESS':
            status_colored = Colors.GREEN + status + Colors.RESET
            cost = f"{Colors.YELLOW}{result['cost']:.2f}{Colors.RESET}"
            visited = f"{Colors.CYAN}{result['visited']}{Colors.RESET}"
            time_ms = f"{Colors.MAGENTA}{result['time']:.4f}{Colors.RESET}"
        else:
            status_colored = Colors.RED + status + Colors.RESET
            cost = f"{Colors.GRAY}-{Colors.RESET}"
            visited = f"{Colors.GRAY}-{Colors.RESET}"
            time_ms = f"{Colors.GRAY}-{Colors.RESET}"
        
        print(f"{algo:<25} {status_colored:<20} {cost:<22} {visited:<22} {time_ms:<22}")
    
    print(Colors.CYAN + "="*80 + Colors.RESET)

def run_single_algorithm(grid_world, algo_choice, visualize=True):
    delay = 0.3
    
    print(f"\n{Colors.YELLOW}Menjalankan algoritma...{Colors.RESET}")
    start_time = time.perf_counter()
    
    if algo_choice == 1:
        solver = BreadthFirstSearch(grid_world, visualize=visualize, delay=delay)
        algo_name = "BFS"
    elif algo_choice == 2:
        solver = UniformCostSearch(grid_world, visualize=visualize, delay=delay)
        algo_name = "UCS"
    elif algo_choice == 3:
        solver = AStar(grid_world, heuristic_type='manhattan', visualize=visualize, delay=delay)
        algo_name = "A* (Manhattan)"
    else:
        solver = AStar(grid_world, heuristic_type='euclidean', visualize=visualize, delay=delay)
        algo_name = "A* (Euclidean)"
    
    path, cost, visited = solver.search()
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000
    
    if path:
        print(f"\n{Colors.BOLD}{Colors.GREEN}Hasil {algo_name}:{Colors.RESET}")
        print(f"Status: {Colors.GREEN}SUCCESS{Colors.RESET}")
        print(f"Total Cost: {Colors.YELLOW}{cost}{Colors.RESET}")
        print(f"Nodes Visited: {Colors.CYAN}{visited}{Colors.RESET}")
        print(f"Time: {Colors.MAGENTA}{execution_time:.4f} ms{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}Visualisasi Jalur Final:{Colors.RESET}")
        grid_world.visualize(path=path)
    else:
        print(f"\n{Colors.RED}Status: FAILED (No Path){Colors.RESET}")

def run_all_algorithms(grid_world):
    results = []
    
    print(f"\n{Colors.CYAN}Running BFS (Breadth First Search)...{Colors.RESET}")
    start_time = time.perf_counter()
    bfs_solver = BreadthFirstSearch(grid_world, visualize=False)
    path_bfs, cost_bfs, visited_bfs = bfs_solver.search()
    end_time = time.perf_counter()
    
    results.append({
        'algo': 'BFS',
        'status': 'SUCCESS' if path_bfs else 'FAILED',
        'cost': cost_bfs if path_bfs else 0,
        'visited': visited_bfs,
        'time': (end_time - start_time) * 1000,
        'path': path_bfs
    })
    
    print(f"{Colors.CYAN}Running UCS (Uniform Cost Search)...{Colors.RESET}")
    start_time = time.perf_counter()
    ucs_solver = UniformCostSearch(grid_world, visualize=False)
    path_ucs, cost_ucs, visited_ucs = ucs_solver.search()
    end_time = time.perf_counter()
    
    results.append({
        'algo': 'UCS',
        'status': 'SUCCESS' if path_ucs else 'FAILED',
        'cost': cost_ucs if path_ucs else 0,
        'visited': visited_ucs,
        'time': (end_time - start_time) * 1000,
        'path': path_ucs
    })
    
    print(f"{Colors.CYAN}Running A* (Manhattan Heuristic)...{Colors.RESET}")
    start_time = time.perf_counter()
    astar_manhattan = AStar(grid_world, heuristic_type='manhattan', visualize=False)
    path_m, cost_m, visited_m = astar_manhattan.search()
    end_time = time.perf_counter()
    
    results.append({
        'algo': 'A* (Manhattan)',
        'status': 'SUCCESS' if path_m else 'FAILED',
        'cost': cost_m if path_m else 0,
        'visited': visited_m,
        'time': (end_time - start_time) * 1000,
        'path': path_m
    })
    
    print(f"{Colors.CYAN}Running A* (Euclidean Heuristic)...{Colors.RESET}")
    start_time = time.perf_counter()
    astar_euclidean = AStar(grid_world, heuristic_type='euclidean', visualize=False)
    path_e, cost_e, visited_e = astar_euclidean.search()
    end_time = time.perf_counter()
    
    results.append({
        'algo': 'A* (Euclidean)',
        'status': 'SUCCESS' if path_e else 'FAILED',
        'cost': cost_e if path_e else 0,
        'visited': visited_e,
        'time': (end_time - start_time) * 1000,
        'path': path_e
    })
    
    print_comparison_table(results)
    
    return results

if __name__ == "__main__":
    print(Colors.CYAN + "="*60 + Colors.RESET)
    print(Colors.BOLD + Colors.GREEN + "NAVIGASI ROBOT PERTANIAN - GRID WORLD" + Colors.RESET)
    print(Colors.CYAN + "="*60 + Colors.RESET)
    print(f"\n{Colors.BOLD}Legenda Terrain:{Colors.RESET}")
    print(f"  {Colors.WHITE}. = Tanah Kering (Bobot: 1){Colors.RESET}")
    print(f"  {Colors.YELLOW}@ = Tanah Gembur (Bobot: 3){Colors.RESET}")
    print(f"  {Colors.MAGENTA}& = Tanah Lumpur (Bobot: 15){Colors.RESET}")
    print(f"  {Colors.BG_RED}# = Rintangan (Bobot: Infinity){Colors.RESET}")
    print(f"  {Colors.BG_GREEN} S {Colors.RESET} = Start, {Colors.BG_BLUE} G {Colors.RESET} = Goal")
    print(f"\n{Colors.BOLD}Visualisasi Step:{Colors.RESET}")
    print(f"  {Colors.BG_YELLOW} X {Colors.RESET} = Node sedang diproses")
    print(f"  {Colors.GREEN}* = Jalur yang ditemukan{Colors.RESET}")
    
    dataset_files = get_dataset_files()

    if not dataset_files:
        print(f"\n{Colors.RED}Tidak ada dataset ditemukan!{Colors.RESET}")
        exit(1)
    
    while True:
        display_dataset_menu(dataset_files)
        
        try:
            choice = input(f"\n{Colors.BOLD}Pilih dataset (masukkan nomor): {Colors.RESET}").strip()
            
            if choice == '0':
                print(f"\n{Colors.GREEN}Terima kasih! Program selesai.{Colors.RESET}")
                break
            
            choice_idx = int(choice) - 1
            
            if choice_idx < 0 or choice_idx >= len(dataset_files):
                print(f"\n{Colors.RED}Pilihan tidak valid! Silakan coba lagi.{Colors.RESET}")
                continue
                
            selected_file = dataset_files[choice_idx]
            
            print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.GREEN}DATASET: {selected_file}{Colors.RESET}")
            print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")

            content = load_dataset(selected_file)
            if not content:
                continue

            grid_world = GridWorld(content)
            
            print(f"\n{Colors.BOLD}Peta Awal:{Colors.RESET}")
            grid_world.visualize()
            
            while True:
                display_algorithm_menu()
                
                algo_choice = input(f"\n{Colors.BOLD}Pilih algoritma (masukkan nomor): {Colors.RESET}").strip()
                
                if algo_choice == '0':
                    break
                
                try:
                    algo_choice = int(algo_choice)
                    
                    if algo_choice < 1 or algo_choice > 5:
                        print(f"\n{Colors.RED}Pilihan tidak valid!{Colors.RESET}")
                        continue
                    
                    if algo_choice == 5:
                        results = run_all_algorithms(grid_world)
                        best_result = None
                        for result in results:
                            if result['status'] == 'SUCCESS' and 'A*' in result['algo']:
                                best_result = result
                                break
                        
                        if best_result and best_result['path']:
                            print(f"\n{Colors.BOLD}Visualisasi Jalur ({best_result['algo']}):{Colors.RESET}")
                            grid_world.visualize(best_result['path'])
                    else:
                        visualize = input(f"\n{Colors.YELLOW}Aktifkan visualisasi step-by-step? (y/n): {Colors.RESET}").strip().lower() == 'y'
                        run_single_algorithm(grid_world, algo_choice, visualize=visualize)
                    
                    input(f"\n{Colors.GRAY}Tekan Enter untuk melanjutkan...{Colors.RESET}")
                    
                except ValueError:
                    print(f"\n{Colors.RED}Input tidak valid! Masukkan angka.{Colors.RESET}")
                    
            lanjut = input(f"\n{Colors.YELLOW}Apakah ingin mencoba dataset lain? (y/n): {Colors.RESET}").strip().lower()
            if lanjut != 'y':
                print(f"\n{Colors.GREEN}Terima kasih! Program selesai.{Colors.RESET}")
                break
                
        except ValueError:
            print(f"\n{Colors.RED}Input tidak valid! Masukkan angka.{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Program dihentikan oleh user.{Colors.RESET}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")

