# Maze Solver

## Running the Code

To execute the program, navigate to the project directory and use one of the following commands:

```sh
python Src/MazeStartupMain.py
```
or
```sh
cd path/to/MazeStartupMain.py  
python MazeStartupMain.py
```

## Available Options

Upon execution, you will be prompted to choose between two options:

1. **Generate and Solve a New Maze**
    - This option allows you to create a custom maze and solve it using a specific algorithm of your choice.

2. **Predefined Maze Generation and Evaluation**
    - This option evaluates all five algorithms using a predefined set of maze sizes, ranging from **20x20** to **100x100** in increments of 20.
    - It generates an evaluation CSV file, solution plots, and performance graphs, all of which are saved in the respective folder within the project directory.
    - ⚠ **Warning:** Choosing this option will overwrite any existing reports, graphs, and plots with new data.