"""
Maze Solver Game with AI using A* Search Algorithm
"""

from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Dict, Iterable, List, Optional, Tuple
import tkinter as tk
from tkinter import messagebox
import time
import random


Cell = Tuple[int, int]


@dataclass
class MazeStats:
    algorithm: str
    found: bool
    visited_nodes: int
    path_length: int


class MazeSolver:
    def __init__(self, rows: int = 10, cols: int = 10) -> None:
        self.rows = rows
        self.cols = cols
        self.start: Cell = (0, 0)
        self.goal: Cell = (rows - 1, cols - 1)
        self.obstacles = self._generate_random_obstacles(rows, cols)
    
    def _generate_random_obstacles(self, rows: int, cols: int) -> set:
        """Generate random obstacles for the maze"""
        obstacles = set()
        num_obstacles = 15  # Number of obstacle cells
        
        while len(obstacles) < num_obstacles:
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)
            cell = (row, col)
            
            # Don't place obstacles at start or goal
            if cell != self.start and cell != self.goal and cell not in obstacles:
                obstacles.add(cell)
        
        return obstacles

    def toggle_obstacle(self, cell: Cell) -> None:
        if cell in (self.start, self.goal):
            return
        if cell in self.obstacles:
            self.obstacles.remove(cell)
        else:
            self.obstacles.add(cell)

    def solve(self, algorithm: str) -> Tuple[List[Cell], List[Cell], MazeStats]:
        if algorithm == "BFS":
            path, visited = self._bfs()
        elif algorithm == "A*":
            path, visited = self._astar()
        else:
            path, visited = self._hill_climbing()

        return path, visited, MazeStats(
            algorithm=algorithm,
            found=bool(path),
            visited_nodes=len(visited),
            path_length=max(0, len(path) - 1),
        )

    def neighbors(self, cell: Cell) -> Iterable[Cell]:
        row, col = cell
        for next_row, next_col in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)):
            next_cell = (next_row, next_col)
            if 0 <= next_row < self.rows and 0 <= next_col < self.cols and next_cell not in self.obstacles:
                yield next_cell

    def heuristic(self, cell: Cell) -> int:
        return abs(cell[0] - self.goal[0]) + abs(cell[1] - self.goal[1])

    def reconstruct_path(self, parent: Dict[Cell, Optional[Cell]], end: Cell) -> List[Cell]:
        path = [end]
        current = end
        while parent[current] is not None:
            current = parent[current]  # type: ignore[assignment]
            path.append(current)
        path.reverse()
        return path

    def _bfs(self) -> Tuple[List[Cell], List[Cell]]:
        queue = deque([self.start])
        parent: Dict[Cell, Optional[Cell]] = {self.start: None}
        visited_order: List[Cell] = []
        while queue:
            current = queue.popleft()
            visited_order.append(current)
            if current == self.goal:
                return self.reconstruct_path(parent, current), visited_order
            for neighbor in self.neighbors(current):
                if neighbor not in parent:
                    parent[neighbor] = current
                    queue.append(neighbor)
        return [], visited_order

    def _astar(self) -> Tuple[List[Cell], List[Cell]]:
        heap: List[Tuple[int, int, Cell]] = [(self.heuristic(self.start), 0, self.start)]
        parent: Dict[Cell, Optional[Cell]] = {self.start: None}
        cost_so_far: Dict[Cell, int] = {self.start: 0}
        visited_order: List[Cell] = []
        while heap:
            _, cost, current = heappop(heap)
            if current in visited_order:
                continue
            visited_order.append(current)
            if current == self.goal:
                return self.reconstruct_path(parent, current), visited_order
            for neighbor in self.neighbors(current):
                next_cost = cost + 1
                if neighbor not in cost_so_far or next_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = next_cost
                    parent[neighbor] = current
                    heappush(heap, (next_cost + self.heuristic(neighbor), next_cost, neighbor))
        return [], visited_order

    def _hill_climbing(self) -> Tuple[List[Cell], List[Cell]]:
        current = self.start
        parent: Dict[Cell, Optional[Cell]] = {self.start: None}
        visited_order = [current]
        seen = {current}
        while current != self.goal:
            options = [neighbor for neighbor in self.neighbors(current) if neighbor not in seen]
            if not options:
                return [], visited_order
            best = min(options, key=self.heuristic)
            if self.heuristic(best) >= self.heuristic(current):
                return [], visited_order
            parent[best] = current
            current = best
            seen.add(current)
            visited_order.append(current)
        return self.reconstruct_path(parent, current), visited_order


class MazeSolverGame:
    """Maze Solver Game UI with A* Visualization"""
    
    def __init__(self, game_window, parent_window):
        self.game_window = game_window
        self.parent_window = parent_window
        self.game_window.title("Maze Solver - A* Algorithm")
        self.game_window.geometry("800x750")
        self.game_window.configure(bg="#1a1a1a")
        
        # Game variables
        self.GRID_SIZE = 10
        self.CELL_SIZE = 50
        self.maze = MazeSolver(self.GRID_SIZE, self.GRID_SIZE)
        self.path = []
        self.visited = []
        self.current_algorithm = "A*"
        self.solving = False
        
        self.setup_ui()
        self.game_window.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_ui(self):
        """Setup game UI"""
        # Title
        title = tk.Label(
            self.game_window,
            text="🗺️ Maze Solver - A* Search Algorithm",
            font=("Arial", 16, "bold"),
            fg="#00ff00",
            bg="#1a1a1a"
        )
        title.pack(pady=10)
        
        # Controls Frame
        control_frame = tk.Frame(self.game_window, bg="#002200")
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        solve_btn = tk.Button(
            control_frame,
            text="🚀 Solve Maze",
            font=("Arial", 11, "bold"),
            bg="#003300",
            fg="#00ff00",
            command=self.solve_maze
        )
        solve_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        reset_btn = tk.Button(
            control_frame,
            text="🔄 Reset",
            font=("Arial", 11, "bold"),
            bg="#003300",
            fg="#00ff00",
            command=self.reset_maze
        )
        reset_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        back_btn = tk.Button(
            control_frame,
            text="🏠 Back",
            font=("Arial", 11, "bold"),
            bg="#003300",
            fg="#00ff00",
            command=self.on_close
        )
        back_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Canvas for maze
        self.canvas = tk.Canvas(
            self.game_window,
            width=self.GRID_SIZE * self.CELL_SIZE,
            height=self.GRID_SIZE * self.CELL_SIZE,
            bg="#000000",
            highlightthickness=2,
            highlightbackground="#00ff00"
        )
        self.canvas.pack(pady=10)
        
        # Stats Frame
        stats_frame = tk.Frame(self.game_window, bg="#002200")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Algorithm: A* | Status: Ready\nVisited Nodes: 0 | Path Length: 0",
            font=("Arial", 10),
            fg="#00dd00",
            bg="#002200",
            justify=tk.LEFT
        )
        self.stats_label.pack(pady=10)
        
        # Draw initial maze
        self.draw_maze()
    
    def draw_maze(self):
        """Draw the maze grid"""
        self.canvas.delete("all")
        
        # Draw grid
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                x1 = j * self.CELL_SIZE
                y1 = i * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                
                # Determine cell color
                if (i, j) == self.maze.start:
                    color = "#00ff00"  # Start - Green
                elif (i, j) == self.maze.goal:
                    color = "#ff0000"  # Goal - Red
                elif (i, j) in self.maze.obstacles:
                    color = "#444444"  # Obstacle - Gray
                elif (i, j) in self.path:
                    color = "#ffff00"  # Path - Yellow
                elif (i, j) in self.visited:
                    color = "#0088ff"  # Visited - Light Blue
                else:
                    color = "#1a1a1a"  # Empty - Dark
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#333333")
    
    def solve_maze(self):
        """Solve the maze using selected algorithm"""
        if self.solving:
            return
        
        self.solving = True
        self.path = []
        self.visited = []
        
        # Solve
        self.path, self.visited, stats = self.maze.solve(self.current_algorithm)
        
        # Update UI
        self.draw_maze()
        
        if self.path:
            message = f"✅ Path Found!\n\nAlgorithm: {stats.algorithm}\nVisited Nodes: {stats.visited_nodes}\nPath Length: {stats.path_length}"
            messagebox.showinfo("Success", message)
        else:
            messagebox.showinfo("No Solution", f"No path found using {stats.algorithm}")
        
        self.stats_label.config(
            text=f"Algorithm: {stats.algorithm} | Status: Solved\nVisited Nodes: {stats.visited_nodes} | Path Length: {stats.path_length}"
        )
        
        self.solving = False
    
    def reset_maze(self):
        """Reset the maze"""
        self.maze = MazeSolver(self.GRID_SIZE, self.GRID_SIZE)
        self.path = []
        self.visited = []
        self.draw_maze()
        self.stats_label.config(
            text="Algorithm: A* | Status: Ready\nVisited Nodes: 0 | Path Length: 0"
        )
    
    def on_close(self):
        """Close the game window"""
        self.game_window.destroy()
        self.parent_window.deiconify()
