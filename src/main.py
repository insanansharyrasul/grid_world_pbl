from grid_environment import GridWorld, Colors
from a_star import AStarSearch
from ucs import UniformCostSearch
from bfs import BreadthFirstSearch

import os
import time

def load_dataset(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_path, "..", "datasets", filename)

    try:
        with open(dataset_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(
            f"{Colors.RED}Error: File {filename} tidak ditemukan di {dataset_path}{Colors.RESET}"
        )
        return None


def get_dataset_files():
    base_path = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_path, "..", "datasets")

    if not os.path.exists(dataset_dir):
        return []

    files = [
        f for f in os.listdir(dataset_dir) if f.endswith(".txt") and f != "README.txt"
    ]
    return sorted(files)


def display_dataset_menu(dataset_files):
    print("\n" + Colors.CYAN + "=" * 60 + Colors.RESET)
    print(Colors.BOLD + Colors.BLUE + "DAFTAR DATASET TERSEDIA" + Colors.RESET)
    print(Colors.CYAN + "=" * 60 + Colors.RESET)

    for idx, filename in enumerate(dataset_files, 1):
        print(f"  {Colors.GREEN}{idx}.{Colors.RESET} {filename}")

    print(f"  {Colors.RED}0.{Colors.RESET} Keluar")
    print(Colors.CYAN + "=" * 60 + Colors.RESET)


def display_algorithm_menu():
    print("\n" + Colors.CYAN + "=" * 60 + Colors.RESET)
    print(Colors.BOLD + Colors.BLUE + "PILIH ALGORITMA" + Colors.RESET)
    print(Colors.CYAN + "=" * 60 + Colors.RESET)
    print(f"  {Colors.GREEN}1.{Colors.RESET} BFS (Breadth-First Search)")
    print(f"  {Colors.GREEN}2.{Colors.RESET} UCS (Uniform Cost Search)")
    print(f"  {Colors.GREEN}3.{Colors.RESET} A* (Manhattan Heuristic)")
    print(f"  {Colors.GREEN}4.{Colors.RESET} A* (Euclidean Heuristic)")
    print(f"  {Colors.GREEN}5.{Colors.RESET} Run All Algorithms (Comparison)")
    print(f"  {Colors.RED}0.{Colors.RESET} Kembali")
    print(Colors.CYAN + "=" * 60 + Colors.RESET)


def print_comparison_table(results):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}TABEL PERBANDINGAN ALGORITMA{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.RESET}")

    print(
        f"\n{Colors.BOLD}{'Algoritma':<20} {'Status':<12} {'Cost':<10} {'Nodes':<10} {'Time (ms)':<15}{Colors.RESET}"
    )
    print(f"{Colors.CYAN}{'-' * 80}{Colors.RESET}")

    for result in results:
        algo = result["algo"]

        if result["status"] == "SUCCESS":
            status = f"{Colors.GREEN}{result['status']:<12}{Colors.RESET}"
            cost = f"{Colors.YELLOW}{result['cost']:<10.2f}{Colors.RESET}"
            visited = f"{Colors.CYAN}{result['visited']:<10}{Colors.RESET}"
            time_ms = f"{Colors.MAGENTA}{result['time']:<15.4f}{Colors.RESET}"
        else:
            status = f"{Colors.RED}{result['status']:<12}{Colors.RESET}"
            cost = f"{Colors.GRAY}{'-':<10}{Colors.RESET}"
            visited = f"{Colors.GRAY}{'-':<10}{Colors.RESET}"
            time_ms = f"{Colors.GRAY}{'-':<15}{Colors.RESET}"

        print(f"{algo:<20} {status} {cost} {visited} {time_ms}")

    print(f"{Colors.CYAN}{'=' * 80}{Colors.RESET}")


def print_result_summary(algo_name, path, cost, visited, execution_time):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}RINGKASAN HASIL - {algo_name}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")

    if path:
        print(
            f"\n{Colors.BOLD}Status:{Colors.RESET} {Colors.GREEN}SUCCESS - Jalur ditemukan!{Colors.RESET}"
        )
        print(
            f"{Colors.BOLD}Total Cost:{Colors.RESET} {Colors.YELLOW}{cost}{Colors.RESET}"
        )
        print(
            f"{Colors.BOLD}Nodes Visited:{Colors.RESET} {Colors.CYAN}{visited}{Colors.RESET}"
        )
        print(
            f"{Colors.BOLD}Path Length:{Colors.RESET} {Colors.MAGENTA}{len(path)} langkah{Colors.RESET}"
        )
        print(
            f"{Colors.BOLD}Execution Time:{Colors.RESET} {Colors.MAGENTA}{execution_time:.4f} ms{Colors.RESET}"
        )

        nodes_per_ms = visited / execution_time if execution_time > 0 else 0
        print(
            f"{Colors.BOLD}Throughput:{Colors.RESET} {Colors.CYAN}{nodes_per_ms:.2f} nodes/ms{Colors.RESET}"
        )

        print(f"\n{Colors.BOLD}Jalur yang Ditemukan:{Colors.RESET}")
        path_str = " -> ".join([f"({r},{c})" for r, c in path])
        print(f"{Colors.GREEN}{path_str}{Colors.RESET}")

        print(f"\n{Colors.BOLD}Format Output Standar:{Colors.RESET}")
        print(f"Path ({algo_name}, cost={cost}): {path_str}")

        print(f"\n{Colors.BOLD}Ringkasan:{Colors.RESET}")
        print(f"{algo_name}: {visited} node, cost {cost}, {execution_time:.4f} ms")
    else:
        print(
            f"\n{Colors.BOLD}Status:{Colors.RESET} {Colors.RED}FAILED - Tidak ada jalur!{Colors.RESET}"
        )
        print(
            f"{Colors.BOLD}Nodes Visited:{Colors.RESET} {Colors.CYAN}{visited}{Colors.RESET}"
        )
        print(
            f"{Colors.BOLD}Execution Time:{Colors.RESET} {Colors.MAGENTA}{execution_time:.4f} ms{Colors.RESET}"
        )

    print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}\n")


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
        solver = AStar(
            grid_world, heuristic_type="manhattan", visualize=visualize, delay=delay
        )
        algo_name = "A* (Manhattan)"
    else:
        solver = AStar(
            grid_world, heuristic_type="euclidean", visualize=visualize, delay=delay
        )
        algo_name = "A* (Euclidean)"

    path, cost, visited = solver.search()
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000

    print_result_summary(algo_name, path, cost, visited, execution_time)

    if path:
        print(f"{Colors.BOLD}Visualisasi Jalur Final:{Colors.RESET}")
        grid_world.visualize(path=path)


def run_all_algorithms(grid_world):
    results = []

    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}MENJALANKAN SEMUA ALGORITMA{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}\n")

    print(f"{Colors.CYAN}[1/4] Running BFS (Breadth First Search)...{Colors.RESET}")
    start_time = time.perf_counter()
    bfs_solver = BreadthFirstSearch(grid_world, visualize=False)
    path_bfs, cost_bfs, visited_bfs = bfs_solver.search()
    end_time = time.perf_counter()
    time_bfs = (end_time - start_time) * 1000

    if path_bfs:
        print(
            f"{Colors.GREEN}✓ BFS: {visited_bfs} nodes, cost {cost_bfs}, {time_bfs:.4f} ms{Colors.RESET}"
        )
    else:
        print(f"{Colors.RED}✗ BFS: No path found{Colors.RESET}")

    results.append(
        {
            "algo": "BFS",
            "status": "SUCCESS" if path_bfs else "FAILED",
            "cost": cost_bfs if path_bfs else 0,
            "visited": visited_bfs,
            "time": time_bfs,
            "path": path_bfs,
        }
    )

    print(f"\n{Colors.CYAN}[2/4] Running UCS (Uniform Cost Search)...{Colors.RESET}")
    start_time = time.perf_counter()
    ucs_solver = UniformCostSearch(grid_world, visualize=False)
    path_ucs, cost_ucs, visited_ucs = ucs_solver.search()
    end_time = time.perf_counter()
    time_ucs = (end_time - start_time) * 1000

    if path_ucs:
        print(
            f"{Colors.GREEN}✓ UCS: {visited_ucs} nodes, cost {cost_ucs}, {time_ucs:.4f} ms{Colors.RESET}"
        )
    else:
        print(f"{Colors.RED}✗ UCS: No path found{Colors.RESET}")

    results.append(
        {
            "algo": "UCS",
            "status": "SUCCESS" if path_ucs else "FAILED",
            "cost": cost_ucs if path_ucs else 0,
            "visited": visited_ucs,
            "time": time_ucs,
            "path": path_ucs,
        }
    )

    print(f"\n{Colors.CYAN}[3/4] Running A* (Manhattan Heuristic)...{Colors.RESET}")
    start_time = time.perf_counter()
    astar_manhattan = AStar(grid_world, heuristic_type="manhattan", visualize=False)
    path_m, cost_m, visited_m = astar_manhattan.search()
    end_time = time.perf_counter()
    time_m = (end_time - start_time) * 1000

    if path_m:
        print(
            f"{Colors.GREEN}✓ A* (Manhattan): {visited_m} nodes, cost {cost_m}, {time_m:.4f} ms{Colors.RESET}"
        )
    else:
        print(f"{Colors.RED}✗ A* (Manhattan): No path found{Colors.RESET}")

    results.append(
        {
            "algo": "A* (Manhattan)",
            "status": "SUCCESS" if path_m else "FAILED",
            "cost": cost_m if path_m else 0,
            "visited": visited_m,
            "time": time_m,
            "path": path_m,
        }
    )

    print(f"\n{Colors.CYAN}[4/4] Running A* (Euclidean Heuristic)...{Colors.RESET}")
    start_time = time.perf_counter()
    astar_euclidean = AStar(grid_world, heuristic_type="euclidean", visualize=False)
    path_e, cost_e, visited_e = astar_euclidean.search()
    end_time = time.perf_counter()
    time_e = (end_time - start_time) * 1000

    if path_e:
        print(
            f"{Colors.GREEN}✓ A* (Euclidean): {visited_e} nodes, cost {cost_e}, {time_e:.4f} ms{Colors.RESET}"
        )
    else:
        print(f"{Colors.RED}✗ A* (Euclidean): No path found{Colors.RESET}")

    results.append(
        {
            "algo": "A* (Euclidean)",
            "status": "SUCCESS" if path_e else "FAILED",
            "cost": cost_e if path_e else 0,
            "visited": visited_e,
            "time": time_e,
            "path": path_e,
        }
    )

    print_comparison_table(results)

    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}ANALISIS PERFORMA ALGORITMA{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.RESET}")

    successful_results = [r for r in results if r["status"] == "SUCCESS"]

    if successful_results:
        print(f"\n{Colors.BOLD}1. ANALISIS WAKTU EKSEKUSI:{Colors.RESET}")
        fastest = min(successful_results, key=lambda x: x["time"])
        slowest = max(successful_results, key=lambda x: x["time"])
        avg_time = sum(r["time"] for r in successful_results) / len(successful_results)

        print(
            f"   {Colors.GREEN}Tercepat:{Colors.RESET} {Colors.YELLOW}{fastest['algo']}{Colors.RESET} - {Colors.MAGENTA}{fastest['time']:.4f} ms{Colors.RESET}"
        )
        print(
            f"   {Colors.RED}Terlambat:{Colors.RESET} {Colors.YELLOW}{slowest['algo']}{Colors.RESET} - {Colors.MAGENTA}{slowest['time']:.4f} ms{Colors.RESET}"
        )
        print(
            f"   {Colors.CYAN}Rata-rata:{Colors.RESET} {Colors.MAGENTA}{avg_time:.4f} ms{Colors.RESET}"
        )

        if slowest["time"] > 0:
            speedup = slowest["time"] / fastest["time"]
            print(
                f"   {Colors.BOLD}Speedup:{Colors.RESET} {fastest['algo']} {Colors.GREEN}{speedup:.2f}x lebih cepat{Colors.RESET} dari {slowest['algo']}"
            )

        print(f"\n{Colors.BOLD}2. ANALISIS EFISIENSI NODE:{Colors.RESET}")
        most_efficient = min(successful_results, key=lambda x: x["visited"])
        least_efficient = max(successful_results, key=lambda x: x["visited"])
        avg_nodes = sum(r["visited"] for r in successful_results) / len(
            successful_results
        )

        print(
            f"   {Colors.GREEN}Paling Efisien:{Colors.RESET} {Colors.YELLOW}{most_efficient['algo']}{Colors.RESET} - {Colors.CYAN}{most_efficient['visited']} nodes{Colors.RESET}"
        )
        print(
            f"   {Colors.RED}Kurang Efisien:{Colors.RESET} {Colors.YELLOW}{least_efficient['algo']}{Colors.RESET} - {Colors.CYAN}{least_efficient['visited']} nodes{Colors.RESET}"
        )
        print(
            f"   {Colors.CYAN}Rata-rata:{Colors.RESET} {Colors.CYAN}{avg_nodes:.1f} nodes{Colors.RESET}"
        )

        if least_efficient["visited"] > 0:
            efficiency_ratio = (
                (least_efficient["visited"] - most_efficient["visited"])
                / least_efficient["visited"]
                * 100
            )
            print(
                f"   {Colors.BOLD}Efisiensi:{Colors.RESET} {most_efficient['algo']} mengeksplorasi {Colors.GREEN}{efficiency_ratio:.1f}% lebih sedikit{Colors.RESET} node"
            )

        print(f"\n{Colors.BOLD}3. ANALISIS OPTIMALITY (COST):{Colors.RESET}")
        best_cost = min(successful_results, key=lambda x: x["cost"])
        worst_cost = max(successful_results, key=lambda x: x["cost"])

        print(
            f"   {Colors.GREEN}Cost Terendah:{Colors.RESET} {Colors.YELLOW}{best_cost['algo']}{Colors.RESET} - {Colors.YELLOW}{best_cost['cost']}{Colors.RESET}"
        )
        print(
            f"   {Colors.RED}Cost Tertinggi:{Colors.RESET} {Colors.YELLOW}{worst_cost['algo']}{Colors.RESET} - {Colors.YELLOW}{worst_cost['cost']}{Colors.RESET}"
        )

        optimal_algos = [
            r["algo"] for r in successful_results if r["cost"] == best_cost["cost"]
        ]
        if len(optimal_algos) > 1:
            print(
                f"   {Colors.CYAN}Algoritma Optimal:{Colors.RESET} {', '.join(optimal_algos)} (semua menemukan path optimal)"
            )

        print(f"\n{Colors.BOLD}4. RINGKASAN HASIL:{Colors.RESET}")
        for result in results:
            if result["status"] == "SUCCESS":
                print(
                    f"   {result['algo']}: {result['visited']} node, cost {result['cost']}, {result['time']:.4f} ms"
                )
            else:
                print(f"   {result['algo']}: {Colors.RED}No path found{Colors.RESET}")

        print(f"\n{Colors.BOLD}{Colors.GREEN}ALGORITMA TERBAIK:{Colors.RESET}")

        best_overall = min(
            successful_results, key=lambda x: (x["cost"], x["visited"], x["time"])
        )
        print(f"   {Colors.YELLOW}{best_overall['algo']}{Colors.RESET}")
        print(f"   └─ Cost: {Colors.YELLOW}{best_overall['cost']}{Colors.RESET}")
        print(f"   └─ Nodes: {Colors.CYAN}{best_overall['visited']}{Colors.RESET}")
        print(
            f"   └─ Time: {Colors.MAGENTA}{best_overall['time']:.4f} ms{Colors.RESET}"
        )

        if best_overall["path"]:
            path_str = " -> ".join([f"({r},{c})" for r, c in best_overall["path"]])
            print(
                f"\n{Colors.BOLD}Path ({best_overall['algo']}, cost={best_overall['cost']}):{Colors.RESET}"
            )
            print(f"{Colors.GREEN}{path_str}{Colors.RESET}")
    else:
        print(
            f"\n{Colors.RED}Tidak ada algoritma yang berhasil menemukan jalur!{Colors.RESET}"
        )

    print(f"{Colors.CYAN}{'=' * 80}{Colors.RESET}\n")

    return results


if __name__ == "__main__":
    print(Colors.CYAN + "=" * 60 + Colors.RESET)
    print(
        Colors.BOLD
        + Colors.GREEN
        + "NAVIGASI ROBOT PERTANIAN - GRID WORLD"
        + Colors.RESET
    )
    print(Colors.CYAN + "=" * 60 + Colors.RESET)
    print(f"\n{Colors.BOLD}Legenda Terrain:{Colors.RESET}")
    print(f"  {Colors.WHITE}. = Tanah Kering (Bobot: 1){Colors.RESET}")
    print(f"  {Colors.YELLOW}@ = Tanah Gembur (Bobot: 3){Colors.RESET}")
    print(f"  {Colors.MAGENTA}& = Tanah Lumpur (Bobot: 15){Colors.RESET}")
    print(f"  {Colors.BG_RED}# = Rintangan (Bobot: Infinity){Colors.RESET}")
    print(
        f"  {Colors.BG_GREEN} S {Colors.RESET} = Start, {Colors.BG_BLUE} G {Colors.RESET} = Goal"
    )
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
            choice = input(
                f"\n{Colors.BOLD}Pilih dataset (masukkan nomor): {Colors.RESET}"
            ).strip()

            if choice == "0":
                print(f"\n{Colors.GREEN}Terima kasih! Program selesai.{Colors.RESET}")
                break

            choice_idx = int(choice) - 1

            if choice_idx < 0 or choice_idx >= len(dataset_files):
                print(
                    f"\n{Colors.RED}Pilihan tidak valid! Silakan coba lagi.{Colors.RESET}"
                )
                continue

            selected_file = dataset_files[choice_idx]

            print(f"\n{Colors.CYAN}{'=' * 60}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.GREEN}DATASET: {selected_file}{Colors.RESET}")
            print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}")

            content = load_dataset(selected_file)
            if not content:
                continue

            grid_world = GridWorld(content)

            print(f"\n{Colors.BOLD}Peta Awal:{Colors.RESET}")
            grid_world.visualize()

            while True:
                display_algorithm_menu()

                algo_choice = input(
                    f"\n{Colors.BOLD}Pilih algoritma (masukkan nomor): {Colors.RESET}"
                ).strip()

                if algo_choice == "0":
                    break

                try:
                    algo_choice = int(algo_choice)

                    if algo_choice < 1 or algo_choice > 5:
                        print(f"\n{Colors.RED}Pilihan tidak valid!{Colors.RESET}")
                        continue

                    if algo_choice == 5:
                        print(
                            f"\n{Colors.BOLD}{Colors.YELLOW}Menjalankan semua algoritma...{Colors.RESET}\n"
                        )
                        results = run_all_algorithms(grid_world)

                        best_result = None
                        for result in results:
                            if result["status"] == "SUCCESS":
                                if (
                                    best_result is None
                                    or result["cost"] < best_result["cost"]
                                ):
                                    best_result = result

                        if best_result and best_result["path"]:
                            print(
                                f"\n{Colors.BOLD}{Colors.GREEN}Visualisasi Jalur Terbaik ({best_result['algo']}):{Colors.RESET}"
                            )
                            grid_world.visualize(
                                path=best_result["path"], clear_screen=False
                            )
                        else:
                            print(
                                f"\n{Colors.RED}Tidak ada jalur yang ditemukan oleh algoritma manapun!{Colors.RESET}"
                            )
                    else:
                        visualize = (
                            input(
                                f"\n{Colors.YELLOW}Aktifkan visualisasi step-by-step? (y/n): {Colors.RESET}"
                            )
                            .strip()
                            .lower()
                            == "y"
                        )
                        run_single_algorithm(
                            grid_world, algo_choice, visualize=visualize
                        )

                    input(
                        f"\n{Colors.GRAY}Tekan Enter untuk melanjutkan...{Colors.RESET}"
                    )

                except ValueError:
                    print(
                        f"\n{Colors.RED}Input tidak valid! Masukkan angka.{Colors.RESET}"
                    )

            lanjut = (
                input(
                    f"\n{Colors.YELLOW}Apakah ingin mencoba dataset lain? (y/n): {Colors.RESET}"
                )
                .strip()
                .lower()
            )
            if lanjut != "y":
                print(f"\n{Colors.GREEN}Terima kasih! Program selesai.{Colors.RESET}")
                break

        except ValueError:
            print(f"\n{Colors.RED}Input tidak valid! Masukkan angka.{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Program dihentikan oleh user.{Colors.RESET}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
