import matplotlib.pyplot as plt
import numpy as np
import heapq
from PIL import Image

# Load maze from an image file and convert to a binary numpy array.
def load_maze(filename, maze_width, maze_height):
    img = Image.open(filename).convert('L')
    img_resized = img.resize((maze_width * 2 + 1, maze_height * 2 + 1))
    maze = np.array(img_resized)
    maze = np.where(maze < 128, 1, 0)  # 1 for walls, 0 for paths
    return maze

# Return valid neighboring cells (not walls) for position (x, y).
def get_neighbors(x, y, maze):
    neighbors = []
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < maze.shape[1] and 0 <= ny < maze.shape[0] and maze[nx, ny] == 0:
            neighbors.append((nx, ny))
    return neighbors

# Solve maze using Depth-First Search (DFS).
def solve_dfs(maze, start, end):
    stack = [start]
    parent_map = {}
    while stack:
        current = stack.pop()
        if current == end:
            path = []
            while current != start:
                path.append(current)
                current = parent_map[current]
            path.append(start)
            path.reverse()
            return path
        for neighbor in get_neighbors(current[0], current[1], maze):
            if neighbor not in parent_map:
                parent_map[neighbor] = current
                stack.append(neighbor)
    return None

# Solve maze using Breadth-First Search (BFS).
def solve_bfs(maze, start, end):
    from collections import deque
    queue = deque([start])
    parent_map = {}
    while queue:
        current = queue.popleft()
        if current == end:
            path = []
            while current != start:
                path.append(current)
                current = parent_map[current]
            path.append(start)
            path.reverse()
            return path
        for neighbor in get_neighbors(current[0], current[1], maze):
            if neighbor not in parent_map:
                parent_map[neighbor] = current
                queue.append(neighbor)
    return None

# Solve maze using A* search algorithm.
def solve_astar(maze, start, end):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    open_list = []
    heapq.heappush(open_list, (heuristic(start, end), 0, start))
    g_costs = {start: 0}
    parent_map = {}
    while open_list:
        _, current_g, current = heapq.heappop(open_list)
        if current == end:
            path = []
            while current != start:
                path.append(current)
                current = parent_map[current]
            path.append(start)
            path.reverse()
            return path
        for neighbor in get_neighbors(current[0], current[1], maze):
            new_g = current_g + 1
            if neighbor not in g_costs or new_g < g_costs[neighbor]:
                g_costs[neighbor] = new_g
                f_cost = new_g + heuristic(neighbor, end)
                heapq.heappush(open_list, (f_cost, new_g, neighbor))
                parent_map[neighbor] = current
    return None

# Solve maze using MDP Value Iteration.
def value_iteration(maze, start, end, gamma=0.99, theta=1e-4):
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    action_names = ['↑', '↓', '←', '→']
    rows, cols = len(maze), len(maze[0])
    reward_goal = 1000
    reward_default = -0.1
    reward_wall = -1
    values = np.zeros((rows, cols))
    policy = np.full((rows, cols), ' ')

    def get_reward(state):
        if state == end:
            return reward_goal
        elif maze[state[0]][state[1]] == 1:
            return reward_wall
        else:
            return reward_default

    def get_next_state(state, action):
        new_state = (state[0] + action[0], state[1] + action[1])
        if 0 <= new_state[0] < rows and 0 <= new_state[1] < cols and maze[new_state[0]][new_state[1]] != 1:
            return new_state
        else:
            return state

    # Run value iteration and count iterations until convergence.
    def run_value_iteration():
        iteration = 0
        while True:
            delta = 0
            new_values = np.copy(values)
            for i in range(rows):
                for j in range(cols):
                    state = (i, j)
                    if maze[i][j] == 1 or state == end:
                        continue
                    value_actions = []
                    for action in actions:
                        next_state = get_next_state(state, action)
                        reward = get_reward(next_state)
                        value_actions.append(reward + gamma * values[next_state[0]][next_state[1]])
                    new_values[i][j] = max(value_actions)
                    delta = max(delta, abs(new_values[i][j] - values[i][j]))
            values[:, :] = new_values
            iteration += 1
            if delta < theta:
                print(f"Value Iteration converged after {iteration} iterations.")
                return iteration
    iters = run_value_iteration()

    def extract_policy():
        for i in range(rows):
            for j in range(cols):
                state = (i, j)
                if maze[i][j] == 1 or state == end:
                    continue
                best_action = None
                best_value = float('-inf')
                for k, action in enumerate(actions):
                    next_state = get_next_state(state, action)
                    value = get_reward(next_state) + gamma * values[next_state[0]][next_state[1]]
                    if value > best_value:
                        best_value = value
                        best_action = k
                policy[i][j] = action_names[best_action]

    def get_optimal_path():
        path = []
        current = start
        while current != end:
            path.append(current)
            action = policy[current[0]][current[1]]
            action_index = action_names.index(action)
            next_state = get_next_state(current, actions[action_index])
            if next_state == current:
                break
            current = next_state
        path.append(end)
        return path

    extract_policy()
    path = get_optimal_path()
    return path, iters

# Solve maze using MDP Policy Iteration.
def policy_iteration(maze, start, end, gamma=0.99, theta=1e-4):
    maze = np.array(maze)
    rows, cols = maze.shape
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    policy = np.random.choice([0, 1, 2, 3], size=(rows, cols))
    V = np.zeros((rows, cols), dtype=float)

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and maze[x, y] != 1

    policy_iter_count = 0
    while True:
        policy_iter_count += 1
        while True:
            delta = 0
            for i in range(rows):
                for j in range(cols):
                    if maze[i, j] == 1 or (i, j) == end:
                        continue
                    v = V[i, j]
                    a = policy[i, j]
                    dx, dy = actions[a]
                    ni, nj = i + dx, j + dy
                    if is_valid(ni, nj):
                        V[i, j] = -1 + gamma * V[ni, nj]
                    else:
                        V[i, j] = -float('inf')
                    diff = abs(v - V[i, j]) if not (np.isneginf(v) and np.isneginf(V[i, j])) else 0
                    delta = max(delta, diff)
            if delta < theta:
                break
        policy_stable = True
        for i in range(rows):
            for j in range(cols):
                if maze[i, j] == 1 or (i, j) == end:
                    continue
                old_action = policy[i, j]
                action_values = []
                for k, (dx, dy) in enumerate(actions):
                    ni, nj = i + dx, j + dy
                    if is_valid(ni, nj):
                        action_values.append(-1 + gamma * V[ni, nj])
                    else:
                        action_values.append(-float('inf'))
                best_action = int(np.argmax(action_values))
                policy[i, j] = best_action
                if old_action != best_action:
                    policy_stable = False
        if policy_stable:
            print(f"Policy Iteration converged after {policy_iter_count} iterations.")
            break

    path = [start]
    current = start
    max_steps = rows * cols
    steps = 0
    while current != end and steps < max_steps:
        i, j = current
        a = policy[i, j]
        dx, dy = actions[a]
        next_state = (i + dx, j + dy)
        if next_state == current:
            break
        path.append(next_state)
        current = next_state
        steps += 1
    return path, policy_iter_count

# Generate a maze filename based on dimensions.
def get_maze_filename(width, height):
    return f"maze_{width}x{height}.png"

# Draw the solution on the maze, save the image, and return solution length and filename.
def draw_and_save_solution(maze, solution, output_filename, algo_time, width, height, iterations=None):
    maze_copy = maze.copy()
    for x, y in solution:
        maze_copy[x, y] = 2
    plt.imshow(maze_copy, cmap='binary')
    plt.axis('off')
    title = f"Maze_{width}x{height}\nSteps: {len(solution)} | Time: {algo_time:.4f} seconds"
    if iterations is not None:
        title += f" | Iterations: {iterations}"
    plt.title(title, fontsize=14, color='black')
    plt.savefig(output_filename, bbox_inches='tight')
    plt.close()
    print(f"Solution saved as {output_filename}")
    return len(solution), output_filename

# Draw the solution on the maze and display it.
def draw_and_show_solution(maze, solution, algo_time, width, height, iterations=None):
    maze_copy = maze.copy()
    for x, y in solution:
        maze_copy[x, y] = 2
    plt.imshow(maze_copy, cmap='binary')
    plt.axis('off')
    steps_taken = len(solution)
    title = f"Maze_{width}x{height}\nSteps: {steps_taken} | Time: {algo_time:.4f} seconds"
    if iterations is not None:
        title += f" | Iterations: {iterations}"
    plt.title(title, fontsize=14, color='black')
    plt.show()
    return steps_taken
