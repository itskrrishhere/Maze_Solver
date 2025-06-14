# Maze Solver

This project provides a graphical application for generating, solving, and evaluating mazes using multiple algorithms, including DFS, BFS, A*, and Markov Decision Process (MDP) methods (Value Iteration and Policy Iteration).

## Features

- **Maze Generation:** Uses Wilson's algorithm with optional extra paths for more complex mazes.
- **Maze Solving:** Supports DFS, BFS, A*, MDP Value Iteration, and MDP Policy Iteration.
- **Graphical User Interface:** Built with Tkinter for easy interaction.
- **Performance Evaluation:** Automatically benchmarks algorithms on various maze sizes, saving results and plots.
- **Visualization:** Displays and saves maze solutions and performance graphs.

## Getting Started

### Prerequisites

- Python 3.9+
- Required packages: `numpy`, `matplotlib`, `pandas`, `Pillow`, `tkinter`

Install dependencies with:
```sh
pip install numpy matplotlib pandas pillow
```

### Running the Application

From the project root, run:
```sh
python Src/MazeStartupMain.py
```

### Usage

Upon launching, you can:
1. **Generate and Solve a New Maze:**  
   - Specify maze dimensions and select an algorithm.
   - View the generated maze and its solution.

2. **Predefined Maze Generation and Evaluation:**  
   - Automatically generates mazes of various sizes.
   - Solves each maze with all algorithms.
   - Saves solution images and evaluation metrics in the `Src/Evaluation` folder.

### Output

- **Solution Images:** Saved in `Src/Astar`, `Src/BFS`, `Src/DFS`, `Src/MDP_Policy_Iteration`, and `Src/MDP_Value_Iteration`.
- **Evaluation Results:**  
  - CSV file: `Src/Evaluation/algorithm_times.csv`
  - Performance plots:  
    - `time_vs_mazedimension.png`
    - `memory_vs_mazedimension.png`
    - `iterations_vs_mazedimension.png`

## File Structure

- `Src/Maze_generator.py` — Maze generation logic.
- `Src/Maze_solver.py` — Maze solving algorithms and visualization.
- `Src/MazeStartupMain.py` — Main GUI application and evaluation logic.
- `Src/Evaluation/` — Evaluation results and plots.
- `Src/generated_maze/` — Generated maze images.

## Notes

- Choosing the evaluation option will overwrite previous results in the output folders.
- The application supports keyboard shortcut `ESC` to exit.

## License

This project is for educational purposes.