# reference : https://github.com/CaptainFl1nt/WilsonMazeGenerator/blob/main/MazePngGenerator.py
# reference : https://en.wikipedia.org/wiki/Maze_generation_algorithm#:~:text=way%20anywhere%20else.-,Wilson%27s%20algorithm,-%5Bedit%5D

import os
import matplotlib.pyplot as plt
import numpy as np
import random

# Generate a maze using Wilson's algorithm with multiple paths to the exit.
def generate_maze(width, height, extra_paths=2):
    maze = np.ones((2 * height + 1, 2 * width + 1), dtype=int)

    def get_neighbors(x, y):
        neighbors = []
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                neighbors.append((nx, ny))
        return neighbors

    def wilsons_algorithm():
        unvisited = {(x, y) for x in range(width) for y in range(height)}
        start = random.choice(list(unvisited))
        unvisited.remove(start)
        while unvisited:
            current = random.choice(list(unvisited))
            path = [current]
            while current in unvisited:
                next_cell = random.choice(get_neighbors(*current))
                if next_cell in path:
                    cycle_start = path.index(next_cell)
                    path = path[:cycle_start + 1]
                else:
                    path.append(next_cell)
                current = next_cell
            for i in range(len(path) - 1):
                x1, y1 = path[i]
                x2, y2 = path[i + 1]
                maze[2 * y1 + 1][2 * x1 + 1] = 0  # Mark cell as path
                maze[2 * y2 + 1][2 * x2 + 1] = 0
                if x1 == x2:
                    maze[2 * min(y1, y2) + 2][2 * x1 + 1] = 0  # Vertical connection
                else:
                    maze[2 * y1 + 1][2 * min(x1, x2) + 2] = 0  # Horizontal connection
                unvisited.discard(path[i])
            unvisited.discard(path[-1])

    def add_extra_paths(num_paths):
        # Define entrance and exit in grid coordinates (not maze coordinates)
        entrance_grid = (0, 0)  # Corresponds to maze[1][0]
        exit_grid = (width - 1, height - 1)  # Corresponds to maze[-2][-1]

        # Run a simplified random walk to create additional paths
        for _ in range(num_paths):
            # Start near the entrance and aim toward the exit
            current_x, current_y = entrance_grid
            path_cells = [(current_x, current_y)]

            while (current_x, current_y) != exit_grid:
                # Bias movement toward the exit
                dx = 1 if current_x < exit_grid[0] else (-1 if current_x > exit_grid[0] else 0)
                dy = 1 if current_y < exit_grid[1] else (-1 if current_y > exit_grid[1] else 0)

                # Randomly decide to move horizontally or vertically
                if random.random() < 0.5 and dx != 0:
                    next_x = current_x + dx
                    next_y = current_y
                else:
                    next_x = current_x
                    next_y = current_y + dy if dy != 0 else random.choice([-1, 1])

                if 0 <= next_x < width and 0 <= next_y < height:
                    path_cells.append((next_x, next_y))
                    current_x, current_y = next_x, next_y
                else:
                    break  # Stop if we hit a boundary

            # Carve the extra path by removing walls
            for i in range(len(path_cells) - 1):
                x1, y1 = path_cells[i]
                x2, y2 = path_cells[i + 1]
                maze[2 * y1 + 1][2 * x1 + 1] = 0  # Mark cell as path
                maze[2 * y2 + 1][2 * x2 + 1] = 0
                if x1 == x2:
                    maze[2 * min(y1, y2) + 2][2 * x1 + 1] = 0  # Vertical passage
                else:
                    maze[2 * y1 + 1][2 * min(x1, x2) + 2] = 0  # Horizontal passage

    # Generate the base maze with Wilson's algorithm
    wilsons_algorithm()

    # Set entrance and exit
    maze[1][0] = 0   # Entrance at top-left
    maze[-2][-1] = 0  # Exit at bottom-right

    # Add extra paths from entrance to exit
    add_extra_paths(extra_paths)

    return maze

# Display the generated maze.
def draw_generated_maze(maze, width, height):
    plt.figure(figsize=(10, 10))
    plt.imshow(maze, cmap='binary')
    plt.title(f"Maze_{width}x{height} with Multiple Paths\n", fontsize=14, color='black')
    plt.axis('off')
    plt.show()

# Save the generated maze image to a file.
def save_maze_to_file(maze, filename):
    os.makedirs("generated_maze", exist_ok=True)
    plt.figure(figsize=(10, 10))
    plt.imshow(maze, cmap='binary')
    plt.axis('off')
    plt.savefig(f"generated_maze/{filename}", bbox_inches='tight', pad_inches=0)
    plt.close()

