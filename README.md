# ai-maze-solver
Maze-solving AI using DFS, BFS, and A* algorithms with real-time visualization in Python.
# AI Maze Solver Using Search Algorithms

This project demonstrates the implementation of classic AI search algorithms—DFS, BFS, and A*—to solve a grid-based maze.

## 🔍 Project Overview

The objective of this project is to visualize and compare different search algorithms as they attempt to find a path from a start point to a goal in a 2D maze. The algorithms are:

- Depth-First Search (DFS)
- Breadth-First Search (BFS)
- A* Search (with Manhattan Distance heuristic)

## 🎯 Features

- Custom maze design
- Step-by-step visual representation of each algorithm
- Real-time pathfinding and comparison
- Performance benchmarking (time and path length)

## 📁 Folder Structure

ai-maze-solver/
│
├── main.py # Main game and algorithm controller
├── maze.py # Maze generation and drawing
├── dfs.py # Depth-First Search implementation
├── bfs.py # Breadth-First Search implementation
├── astar.py # A* Search implementation
├── utils.py # Utility functions (like heuristics, timers, etc.)
├── assets/ # Optional: images, fonts, etc.
├── README.md # Project documentation
└── report/AI_Maze_Report.pdf # Final report (converted to PDF)


## 🛠️ Tech Stack

- **Language**: Python
- **Library**: [Pygame](https://www.pygame.org)
- **Version Control**: Git + GitHub

## 🚀 How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/ai-maze-solver.git
    cd ai-maze-solver
    ```

2. Install dependencies:
    ```bash
    pip install pygame
    ```

3. Run the program:
    ```bash
    python main.py
    ```

4. Choose the algorithm to visualize and watch it solve the maze.

## 📊 Algorithm Performance (20x20 Maze)

| Algorithm | Avg. Time (s) | Path Length |
|-----------|---------------|-------------|
| DFS       | 0.12          | Variable    |
| BFS       | 0.25          | Optimal     |
| A*        | 0.18          | Optimal     |

## 👨‍💻 Contributors

- **M. Yousuf Rehan** – DFS, BFS, Maze rendering
- **Syed Azmeer Un Nabi** – A* algorithm, heuristic design, GUI animations

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

## 📑 Report

See the [`report/AI_Maze_Report.pdf`](./report/AI_Maze_Report.pdf) for full project documentation and results.
