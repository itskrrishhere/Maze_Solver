import os
import shutil
import time
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import tracemalloc
import matplotlib.pyplot as plt
from Maze_generator import generate_maze, draw_generated_maze, save_maze_to_file
from Maze_solver import (
    solve_dfs,
    solve_bfs,
    solve_astar,
    value_iteration,
    policy_iteration,
    draw_and_show_solution,
    draw_and_save_solution,
    load_maze,
)



class MazeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maze Solver Application")
        self.geometry("500x300")
        self.create_widgets()
        # Bind the ESC key to exit the application
        self.bind("<Escape>", lambda event: self.destroy())

    def create_widgets(self):
        title_label = tk.Label(self, text="Maze Solver", font=("Helvetica", 18))
        title_label.pack(pady=10)

        btn_generate_solve = tk.Button(self, text="Generate New Maze and Solve",
                                       command=self.generate_new_maze_solve, width=40, height=2)
        btn_generate_solve.pack(pady=10)

        btn_predefined = tk.Button(self, text="Predefined Maze Generation and Evaluation",
                                   command=self.solve_pre_generated_maze, width=40, height=2)
        btn_predefined.pack(pady=10)

        btn_exit = tk.Button(self, text="Exit", command=self.destroy, width=20, height=1)
        btn_exit.pack(pady=10)

    def generate_new_maze_solve(self):
        # Popup window for maze dimensions and algorithm selection
        new_window = tk.Toplevel(self)
        new_window.title("Generate and Solve Maze")
        new_window.geometry("500x500")

        tk.Label(new_window, text="Enter Maze Width:").pack(pady=5)
        entry_width = tk.Entry(new_window)
        entry_width.pack(pady=5)

        tk.Label(new_window, text="Enter Maze Height:").pack(pady=5)
        entry_height = tk.Entry(new_window)
        entry_height.pack(pady=5)

        tk.Label(new_window, text="Select Algorithm:").pack(pady=5)
        var_algo = tk.IntVar(value=1)
        tk.Radiobutton(new_window, text="DFS", variable=var_algo, value=1).pack(anchor="w")
        tk.Radiobutton(new_window, text="BFS", variable=var_algo, value=2).pack(anchor="w")
        tk.Radiobutton(new_window, text="A*", variable=var_algo, value=3).pack(anchor="w")
        tk.Radiobutton(new_window, text="MDP Value Iteration", variable=var_algo, value=4).pack(anchor="w")
        tk.Radiobutton(new_window, text="MDP Policy Iteration", variable=var_algo, value=5).pack(anchor="w")

        def on_submit():
            try:
                width = int(entry_width.get())
                height = int(entry_height.get())
                algo_option = var_algo.get()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid integer values.")
                return

            # Generate and display the maze
            maze = generate_maze(width, height)
            draw_generated_maze(maze, width, height)
            algorithms = {
                1: solve_dfs,
                2: solve_bfs,
                3: solve_astar,
                4: value_iteration,
                5: policy_iteration
            }
            solve_algorithm = algorithms.get(algo_option)
            start = (1, 0)  # Entrance
            end = (maze.shape[1] - 2, maze.shape[0] - 1)  # Exit

            if solve_algorithm:
                # Show a simple loading indicator
                loading_label = tk.Label(new_window, text="Solving Maze... Please wait.", font=("Helvetica", 12),
                                         fg="blue")
                loading_label.pack(pady=10)
                new_window.update_idletasks()  # Update GUI

                tracemalloc.start()
                start_time = time.time()
                if algo_option in [4, 5]:
                    result = solve_algorithm(maze, start, end)
                    solution = result[0]
                    iterations = result[1]
                else:
                    solution = solve_algorithm(maze, start, end)
                    iterations = None
                algo_time = time.time() - start_time
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                memory_used = peak / 1024  # in KB

                # Remove the loading indicator
                loading_label.destroy()

                if solution:
                    messagebox.showinfo("Success",
                                        f"Solution found in {algo_time:.4f} seconds with {len(solution)} steps!")
                    draw_and_show_solution(maze, solution, algo_time, width, height, iterations)
                else:
                    messagebox.showwarning("No Solution", "No solution found for the generated maze.")
            else:
                messagebox.showerror("Algorithm Error", "Invalid algorithm option selected.")
            new_window.destroy()

        submit_button = tk.Button(new_window, text="Solve Maze", command=on_submit, width=20, height=2)
        submit_button.pack(pady=10)

    def delete_old_folder(self):
        # Helper function to delete old folders and create new ones
        folders = ["generated_maze", "Astar", "BFS", "DFS", "Evaluation", "MDP_Policy_Iteration", "MDP_Value_Iteration"]
        for folder in folders:
            if os.path.exists(folder):
                shutil.rmtree(folder)
            os.makedirs(folder, exist_ok=True)
        messagebox.showinfo("Info", "Old folders deleted and new folders created successfully.")

    def solve_pre_generated_maze(self):
        self.delete_old_folder()
        # Define predefined maze sizes (you can add more sizes here)
        maze_sizes = [(20, 20),(40,40),(60, 60),(80,80),(100, 100)]
        for width, height in maze_sizes:
            maze = generate_maze(width, height)
            draw_generated_maze(maze, width, height)
            save_maze_to_file(maze, f"maze_{width}x{height}.png")
            messagebox.showinfo("Info", f"Maze saved: maze_{width}x{height}.png")

        # Show a simple loading window for evaluation progress
        loading_window = tk.Toplevel(self)
        loading_window.title("Processing Mazes")
        loading_label = tk.Label(loading_window, text="Processing pre-generated mazes... Please wait.",
                                 font=("Helvetica", 14))
        loading_label.pack(pady=20)
        loading_window.update_idletasks()

        # Solve each generated maze using multiple algorithms and collect metrics.
        results = []
        maze_folder = "generated_maze"
        maze_files = [f for f in os.listdir(maze_folder) if f.endswith('.png')]

        for maze_filename in maze_files:
            maze_size_str = maze_filename.split('_')[1].split('.')[0]  # e.g., '100x100'
            maze_width, maze_height = map(int, maze_size_str.split('x'))
            maze = load_maze(os.path.join(maze_folder, maze_filename), maze_width, maze_height)
            start = (1, 0)
            end = (maze.shape[1] - 2, maze.shape[0] - 1)

            # Solve with DFS
            tracemalloc.start()
            start_time = time.time()
            solution_dfs = solve_dfs(maze, start, end)
            dfs_time = time.time() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            dfs_memory = peak / 1024
            if solution_dfs:
                steps_dfs = draw_and_save_solution(maze, solution_dfs, os.path.join("DFS", f"solved_{maze_filename}"),
                                                   dfs_time, maze_width, maze_height)[0]
            else:
                steps_dfs = 0
            results.append({"Maze": maze_filename, "Algorithm": "DFS", "Time in seconds": dfs_time,
                            "Steps": steps_dfs, "Memory (KB)": dfs_memory, "Iterations": None})

            # Solve with BFS
            tracemalloc.start()
            start_time = time.time()
            solution_bfs = solve_bfs(maze, start, end)
            bfs_time = time.time() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            bfs_memory = peak / 1024
            if solution_bfs:
                steps_bfs = draw_and_save_solution(maze, solution_bfs, os.path.join("BFS", f"solved_{maze_filename}"),
                                                   bfs_time, maze_width, maze_height)[0]
            else:
                steps_bfs = 0
            results.append({"Maze": maze_filename, "Algorithm": "BFS", "Time in seconds": bfs_time,
                            "Steps": steps_bfs, "Memory (KB)": bfs_memory, "Iterations": None})

            # Solve with A*
            tracemalloc.start()
            start_time = time.time()
            solution_astar = solve_astar(maze, start, end)
            astar_time = time.time() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            astar_memory = peak / 1024
            if solution_astar:
                steps_astar = draw_and_save_solution(maze, solution_astar, os.path.join("Astar", f"solved_{maze_filename}"),
                                                     astar_time, maze_width, maze_height)[0]
            else:
                steps_astar = 0
            results.append({"Maze": maze_filename, "Algorithm": "A*", "Time in seconds": astar_time,
                            "Steps": steps_astar, "Memory (KB)": astar_memory, "Iterations": None})

            # Solve with MDP Value Iteration
            tracemalloc.start()
            start_time = time.time()
            solution_value_iter, iter_value_iter = value_iteration(maze, start, end)
            value_iter_time = time.time() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            value_iter_memory = peak / 1024
            steps_value_iter = draw_and_save_solution(maze, solution_value_iter,
                                                      os.path.join("MDP_Value_Iteration", f"solved_{maze_filename}"),
                                                      value_iter_time, maze_width, maze_height, iter_value_iter)[0]
            results.append({"Maze": maze_filename, "Algorithm": "MDP Value Iteration", "Time in seconds": value_iter_time,
                            "Steps": steps_value_iter, "Memory (KB)": value_iter_memory, "Iterations": iter_value_iter})

            # Solve with MDP Policy Iteration
            tracemalloc.start()
            start_time = time.time()
            solution_policy_iter, iter_policy = policy_iteration(maze, start, end)
            policy_iter_time = time.time() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            policy_iter_memory = peak / 1024
            steps_policy_iter = draw_and_save_solution(maze, solution_policy_iter,
                                                       os.path.join("MDP_Policy_Iteration", f"solved_{maze_filename}"),
                                                       policy_iter_time, maze_width, maze_height, iter_policy)[0]
            results.append({"Maze": maze_filename, "Algorithm": "MDP Policy Iteration", "Time in seconds": policy_iter_time,
                            "Steps": steps_policy_iter, "Memory (KB)": policy_iter_memory, "Iterations": iter_policy})

        # After processing, destroy the loading window
        loading_window.destroy()
        os.makedirs("Evaluation", exist_ok=True)
        df = pd.DataFrame(results)
        df.to_csv(os.path.join("Evaluation", "algorithm_times.csv"), index=False)
        messagebox.showinfo("Info", "Evaluation results saved to Evaluation/algorithm_times.csv")

        # Generate graphs from the evaluation table.
        self.plot_evaluation_results(os.path.join("Evaluation", "algorithm_times.csv"))

    def plot_evaluation_results(self, csv_file):
        df = pd.read_csv(csv_file)
        # Parse maze dimensions from the filename (assumes format: maze_WIDTHxHEIGHT.png)
        def parse_maze_dimension(filename):
            try:
                size_str = filename.split('_')[1].split('.')[0]  # e.g., '20x20'
                return size_str
            except Exception:
                return None
        df['MazeDimension'] = df['Maze'].apply(parse_maze_dimension)

        # Create a mapping from maze dimension string to a numeric position
        unique_dims = sorted(df['MazeDimension'].unique(), key=lambda x: int(x.split('x')[0]))
        dim_mapping = {dim: i for i, dim in enumerate(unique_dims)}

        # Plot Time vs Maze Dimension for each algorithm.
        plt.figure(figsize=(10, 6))
        for algo in df['Algorithm'].unique():
            subset = df[df['Algorithm'] == algo]
            x = [dim_mapping[d] for d in subset['MazeDimension']]
            plt.plot(x, subset['Time in seconds'], marker='o', linestyle='-', label=algo)
        plt.xlabel("Maze Dimension")
        plt.ylabel("Time (seconds)")
        plt.title("Algorithm Time vs Maze Dimension")
        plt.xticks(list(dim_mapping.values()), list(dim_mapping.keys()))
        plt.legend()
        plt.savefig(os.path.join("Evaluation", "time_vs_mazedimension.png"))
        plt.close()

        # Plot Memory Usage vs Maze Dimension for each algorithm.
        plt.figure(figsize=(10, 6))
        for algo in df['Algorithm'].unique():
            subset = df[df['Algorithm'] == algo]
            x = [dim_mapping[d] for d in subset['MazeDimension']]
            plt.plot(x, subset['Memory (KB)'], marker='o', linestyle='-', label=algo)
        plt.xlabel("Maze Dimension")
        plt.ylabel("Memory Usage (KB)")
        plt.title("Algorithm Memory Usage vs Maze Dimension")
        plt.xticks(list(dim_mapping.values()), list(dim_mapping.keys()))
        plt.legend()
        plt.savefig(os.path.join("Evaluation", "memory_vs_mazedimension.png"))
        plt.close()

        # Plot iterations (for MDP algorithms) vs Maze Dimension.
        mdp_df = df[df['Algorithm'].str.contains("MDP")]
        if not mdp_df.empty:
            plt.figure(figsize=(10, 6))
            for algo in mdp_df['Algorithm'].unique():
                subset = mdp_df[mdp_df['Algorithm'] == algo]
                x = [dim_mapping[d] for d in subset['MazeDimension']]
                plt.plot(x, subset['Iterations'], marker='o', linestyle='-', label=algo)
            plt.xlabel("Maze Dimension")
            plt.ylabel("Iterations for Convergence")
            plt.title("MDP Convergence Iterations vs Maze Dimension")
            plt.xticks(list(dim_mapping.values()), list(dim_mapping.keys()))
            plt.legend()
            plt.savefig(os.path.join("Evaluation", "iterations_vs_mazedimension.png"))
            plt.close()


if __name__ == "__main__":
    app = MazeApp()
    app.mainloop()
