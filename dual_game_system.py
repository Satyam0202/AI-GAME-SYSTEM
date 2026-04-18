from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Tuple

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from maze_solver_ai import Cell, MazeSolver
from tic_tac_toe_ai import TicTacToeAI


class DualGameSystem(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("AI-Based Dual Game System")
        self.geometry("1180x760")
        self.minsize(1080, 700)
        self.configure(bg="#f4efe6")

        container = tk.Frame(self, bg="#f4efe6")
        container.pack(fill="both", expand=True)
        self.frames: Dict[str, tk.Frame] = {}

        for frame_class in (HomePage, TicTacToePage, MazeSolverPage):
            frame = frame_class(container, self)
            self.frames[frame_class.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.show_frame("HomePage")

    def show_frame(self, name: str) -> None:
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()


class PageBase(tk.Frame):
    def __init__(self, parent: tk.Widget, controller: DualGameSystem) -> None:
        super().__init__(parent, bg="#f4efe6")
        self.controller = controller
        self.palette = {
            "bg": "#f4efe6",
            "panel": "#fffaf2",
            "accent": "#136f63",
            "accent_2": "#f4a261",
            "text": "#1f2933",
            "muted": "#52606d",
            "grid": "#d9c7a6",
            "visited": "#9dd9d2",
            "path": "#f4a261",
            "start": "#2a9d8f",
            "goal": "#e76f51",
            "wall": "#5c677d",
        }

    def make_title(self, text: str, subtitle: str) -> None:
        tk.Label(self, text=text, font=("Georgia", 24, "bold"), bg=self.palette["bg"], fg=self.palette["text"]).pack(anchor="w", padx=24, pady=(18, 2))
        tk.Label(self, text=subtitle, font=("Segoe UI", 11), bg=self.palette["bg"], fg=self.palette["muted"]).pack(anchor="w", padx=24, pady=(0, 18))


class HomePage(PageBase):
    def __init__(self, parent: tk.Widget, controller: DualGameSystem) -> None:
        super().__init__(parent, controller)
        self.make_title("AI-Based Dual Game System", "Explore decision making, pathfinding, and algorithm performance in one desktop app.")

        cards = tk.Frame(self, bg=self.palette["bg"])
        cards.pack(fill="both", expand=True, padx=24, pady=20)
        self._build_card(cards, "Tic Tac Toe AI", "Play against an optimal AI using Minimax and Alpha-Beta pruning.", "Learn strategic decision making with live move evaluation.", 0, lambda: controller.show_frame("TicTacToePage"))
        self._build_card(cards, "Maze Solver", "Compare BFS, A*, and Hill Climbing on the same obstacle grid.", "Visualize search progress, path quality, and algorithm tradeoffs.", 1, lambda: controller.show_frame("MazeSolverPage"))

        tk.Label(self, text="Built with Python, Tkinter, and Matplotlib for interactive AI visualization.", font=("Segoe UI", 10, "italic"), bg=self.palette["bg"], fg=self.palette["muted"]).pack(pady=(0, 18))

    def _build_card(self, parent: tk.Widget, title: str, body: str, detail: str, column: int, command) -> None:
        card = tk.Frame(parent, bg=self.palette["panel"], highlightthickness=1, highlightbackground="#eadfcd")
        card.grid(row=0, column=column, sticky="nsew", padx=12, ipadx=12, ipady=12)
        parent.grid_columnconfigure(column, weight=1)

        tk.Label(card, text=title, font=("Georgia", 22, "bold"), bg=self.palette["panel"], fg=self.palette["text"]).pack(anchor="w", padx=20, pady=(20, 10))
        tk.Label(card, text=body, wraplength=360, justify="left", font=("Segoe UI", 12), bg=self.palette["panel"], fg=self.palette["text"]).pack(anchor="w", padx=20)
        tk.Label(card, text=detail, wraplength=360, justify="left", font=("Segoe UI", 11), bg=self.palette["panel"], fg=self.palette["muted"]).pack(anchor="w", padx=20, pady=(12, 24))
        tk.Button(card, text="Open Module", command=command, font=("Segoe UI", 11, "bold"), bg=self.palette["accent"], fg="white", activebackground="#0f5d54", activeforeground="white", relief="flat", padx=18, pady=10, cursor="hand2").pack(anchor="w", padx=20, pady=(0, 20))


class TicTacToePage(PageBase):
    def __init__(self, parent: tk.Widget, controller: DualGameSystem) -> None:
        super().__init__(parent, controller)
        self.ai = TicTacToeAI()
        self.board = self.ai.new_board()
        self.game_over = False
        self.algorithm_var = tk.StringVar(value="Alpha-Beta")
        self.status_var = tk.StringVar(value="Choose an algorithm and make your move.")
        self.stats_var = tk.StringVar(value="Explored nodes: 0 | Score: 0")

        self.make_title("Module 1: Tic Tac Toe AI", "Human vs AI with Minimax and Alpha-Beta pruning.")
        layout = tk.Frame(self, bg=self.palette["bg"])
        layout.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        layout.grid_columnconfigure(0, weight=1)
        layout.grid_columnconfigure(1, weight=1)

        left = tk.Frame(layout, bg=self.palette["panel"], highlightthickness=1, highlightbackground="#eadfcd")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        right = tk.Frame(layout, bg=self.palette["panel"], highlightthickness=1, highlightbackground="#eadfcd")
        right.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        self._build_controls(left)
        self._build_board(right)

    def _build_controls(self, parent: tk.Widget) -> None:
        top = tk.Frame(parent, bg=self.palette["panel"])
        top.pack(fill="x", padx=20, pady=20)
        tk.Button(top, text="Back", command=lambda: self.controller.show_frame("HomePage"), font=("Segoe UI", 10, "bold"), bg="#e9c46a", fg=self.palette["text"], relief="flat", padx=14, pady=8, cursor="hand2").pack(anchor="w")

        tk.Label(parent, text="Algorithm", font=("Segoe UI", 12, "bold"), bg=self.palette["panel"], fg=self.palette["text"]).pack(anchor="w", padx=20)
        ttk.Combobox(parent, textvariable=self.algorithm_var, values=["Minimax", "Alpha-Beta"], state="readonly", font=("Segoe UI", 11)).pack(fill="x", padx=20, pady=(6, 18))
        tk.Button(parent, text="Reset Game", command=self.reset_game, font=("Segoe UI", 11, "bold"), bg=self.palette["accent"], fg="white", relief="flat", padx=18, pady=10, cursor="hand2").pack(anchor="w", padx=20)
        tk.Label(parent, textvariable=self.status_var, wraplength=360, justify="left", font=("Segoe UI", 12), bg=self.palette["panel"], fg=self.palette["text"]).pack(anchor="w", padx=20, pady=(24, 12))
        tk.Label(parent, textvariable=self.stats_var, wraplength=360, justify="left", font=("Segoe UI", 11), bg=self.palette["panel"], fg=self.palette["muted"]).pack(anchor="w", padx=20)

        info = "How it works:\nMinimax checks the full game tree.\nAlpha-Beta gives the same optimal move but prunes unnecessary branches."
        tk.Label(parent, text=info, justify="left", font=("Segoe UI", 11), bg=self.palette["panel"], fg=self.palette["muted"]).pack(anchor="w", padx=20, pady=(26, 0))

    def _build_board(self, parent: tk.Widget) -> None:
        board_frame = tk.Frame(parent, bg=self.palette["panel"])
        board_frame.pack(expand=True)
        self.buttons: List[tk.Button] = []
        for index in range(9):
            button = tk.Button(board_frame, text="", width=5, height=2, font=("Georgia", 26, "bold"), bg="#fffdf8", fg=self.palette["text"], relief="flat", highlightthickness=1, highlightbackground="#eadfcd", command=lambda idx=index: self.player_move(idx), cursor="hand2")
            button.grid(row=index // 3, column=index % 3, padx=8, pady=8, ipadx=12, ipady=12)
            self.buttons.append(button)

    def on_show(self) -> None:
        self._refresh_board()

    def reset_game(self) -> None:
        self.board = self.ai.new_board()
        self.game_over = False
        self.status_var.set("Choose an algorithm and make your move.")
        self.stats_var.set("Explored nodes: 0 | Score: 0")
        self._refresh_board()

    def player_move(self, index: int) -> None:
        if self.game_over or self.board[index]:
            return
        self.board[index] = "X"
        self._refresh_board()
        winner = self.ai.check_winner(self.board)
        if winner:
            self._finish_game(winner)
            return

        ai_move, stats = self.ai.best_move(self.board, self.algorithm_var.get())
        if ai_move is not None:
            self.board[ai_move] = "O"
        self.stats_var.set(f"Explored nodes: {stats.explored_nodes} | Score: {stats.score}")
        self._refresh_board()
        winner = self.ai.check_winner(self.board)
        if winner:
            self._finish_game(winner)
        else:
            self.status_var.set(f"AI played using {stats.algorithm}. Your turn.")

    def _finish_game(self, winner: str) -> None:
        self.game_over = True
        if winner == "Draw":
            self.status_var.set("The match ended in a draw.")
        elif winner == "X":
            self.status_var.set("You won. Nicely played!")
        else:
            self.status_var.set("AI won with optimal play.")

    def _refresh_board(self) -> None:
        for index, button in enumerate(self.buttons):
            symbol = self.board[index]
            button.configure(text=symbol, fg=self.palette["goal"] if symbol == "X" else self.palette["accent"], state="disabled" if self.game_over or symbol else "normal")


class MazeSolverPage(PageBase):
    def __init__(self, parent: tk.Widget, controller: DualGameSystem) -> None:
        super().__init__(parent, controller)
        self.solver = MazeSolver()
        self.algorithm_var = tk.StringVar(value="BFS")
        self.status_var = tk.StringVar(value="Toggle obstacles if you want, then run an algorithm.")
        self.stats_var = tk.StringVar(value="Visited: 0 | Path Length: 0")
        self.animating = False
        self.visited_sequence: List[Cell] = []
        self.path_sequence: List[Cell] = []
        self.visited_index = 0
        self.path_index = 0
        self.visited_cells: List[Cell] = []
        self.path_cells: List[Cell] = []
        self.comparison_records: List[Tuple[str, int, int]] = []

        self.make_title("Module 2: Maze Solver", "Visual comparison of BFS, A*, and Hill Climbing on the same grid.")
        layout = tk.Frame(self, bg=self.palette["bg"])
        layout.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        layout.grid_columnconfigure(0, weight=1)
        layout.grid_columnconfigure(1, weight=1)

        left = tk.Frame(layout, bg=self.palette["panel"], highlightthickness=1, highlightbackground="#eadfcd")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        right = tk.Frame(layout, bg=self.palette["panel"], highlightthickness=1, highlightbackground="#eadfcd")
        right.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        self._build_controls(left)
        self._build_grid(right)
        self._build_chart(left)

    def _build_controls(self, parent: tk.Widget) -> None:
        header = tk.Frame(parent, bg=self.palette["panel"])
        header.pack(fill="x", padx=20, pady=20)
        tk.Button(header, text="Back", command=lambda: self.controller.show_frame("HomePage"), font=("Segoe UI", 10, "bold"), bg="#e9c46a", fg=self.palette["text"], relief="flat", padx=14, pady=8, cursor="hand2").pack(anchor="w")

        tk.Label(parent, text="Select Search Algorithm", font=("Segoe UI", 12, "bold"), bg=self.palette["panel"], fg=self.palette["text"]).pack(anchor="w", padx=20)
        ttk.Combobox(parent, textvariable=self.algorithm_var, values=["BFS", "A*", "Hill Climbing"], state="readonly", font=("Segoe UI", 11)).pack(fill="x", padx=20, pady=(6, 14))

        actions = tk.Frame(parent, bg=self.palette["panel"])
        actions.pack(fill="x", padx=20)
        tk.Button(actions, text="Start", command=self.run_solver, font=("Segoe UI", 11, "bold"), bg=self.palette["accent"], fg="white", relief="flat", padx=18, pady=10, cursor="hand2").pack(side="left", padx=(0, 10))
        tk.Button(actions, text="Reset", command=self.reset_grid, font=("Segoe UI", 11, "bold"), bg=self.palette["accent_2"], fg=self.palette["text"], relief="flat", padx=18, pady=10, cursor="hand2").pack(side="left")

        tk.Label(parent, textvariable=self.status_var, wraplength=360, justify="left", font=("Segoe UI", 12), bg=self.palette["panel"], fg=self.palette["text"]).pack(anchor="w", padx=20, pady=(24, 8))
        tk.Label(parent, textvariable=self.stats_var, wraplength=360, justify="left", font=("Segoe UI", 11), bg=self.palette["panel"], fg=self.palette["muted"]).pack(anchor="w", padx=20, pady=(0, 10))
        tk.Label(parent, text="Tap grid cells to add or remove obstacles before running the search.", wraplength=360, justify="left", font=("Segoe UI", 10), bg=self.palette["panel"], fg=self.palette["muted"]).pack(anchor="w", padx=20)

    def _build_grid(self, parent: tk.Widget) -> None:
        self.cell_size = 44
        self.canvas = tk.Canvas(parent, width=self.solver.cols * self.cell_size, height=self.solver.rows * self.cell_size, bg="white", highlightthickness=0)
        self.canvas.pack(expand=True, padx=20, pady=20)
        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.draw_grid()

    def _build_chart(self, parent: tk.Widget) -> None:
        self.figure = Figure(figsize=(4.6, 2.9), dpi=100)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_title("Algorithm Comparison", fontsize=11)
        self.axes.set_ylabel("Visited Nodes")
        self.axes.set_facecolor("#fffdf8")
        self.figure.patch.set_facecolor(self.palette["panel"])
        self.chart_canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.chart_canvas.get_tk_widget().pack(fill="x", padx=16, pady=(18, 16))
        self.refresh_chart()

    def on_show(self) -> None:
        self.draw_grid()

    def toggle_cell(self, event: tk.Event) -> None:
        if self.animating:
            return
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.solver.rows and 0 <= col < self.solver.cols:
            self.solver.toggle_obstacle((row, col))
            self.visited_cells = []
            self.path_cells = []
            self.status_var.set("Obstacle layout updated. Ready to run.")
            self.draw_grid()

    def reset_grid(self) -> None:
        self.animating = False
        self.solver = MazeSolver()
        self.visited_cells = []
        self.path_cells = []
        self.comparison_records.clear()
        self.status_var.set("Grid reset. Choose an algorithm and start again.")
        self.stats_var.set("Visited: 0 | Path Length: 0")
        self.draw_grid()
        self.refresh_chart()

    def run_solver(self) -> None:
        if self.animating:
            return
        path, visited, stats = self.solver.solve(self.algorithm_var.get())
        self.visited_sequence = visited
        self.path_sequence = path
        self.visited_index = 0
        self.path_index = 0
        self.visited_cells = []
        self.path_cells = []
        self.animating = True
        self.status_var.set(f"Running {stats.algorithm} visualization...")
        self.stats_var.set(f"Visited: {stats.visited_nodes} | Path Length: {stats.path_length}")
        self._record_comparison(stats.algorithm, stats.visited_nodes, stats.path_length)
        self.animate_search(stats.found, stats.algorithm)

    def animate_search(self, found: bool, algorithm: str) -> None:
        if self.visited_index < len(self.visited_sequence):
            self.visited_cells.append(self.visited_sequence[self.visited_index])
            self.visited_index += 1
            self.draw_grid()
            self.after(70, lambda: self.animate_search(found, algorithm))
            return

        if self.path_index < len(self.path_sequence):
            self.path_cells.append(self.path_sequence[self.path_index])
            self.path_index += 1
            self.draw_grid()
            self.after(90, lambda: self.animate_search(found, algorithm))
            return

        self.animating = False
        if found:
            self.status_var.set(f"{algorithm} found a path to the goal.")
        elif algorithm == "Hill Climbing":
            self.status_var.set("Hill Climbing got stuck at a local optimum. Try BFS or A* for reliable search.")
        else:
            self.status_var.set(f"{algorithm} could not reach the goal with this obstacle layout.")

    def _record_comparison(self, algorithm: str, visited_nodes: int, path_length: int) -> None:
        self.comparison_records = [record for record in self.comparison_records if record[0] != algorithm]
        self.comparison_records.append((algorithm, visited_nodes, path_length))
        self.comparison_records.sort(key=lambda item: item[0])
        self.refresh_chart()

    def refresh_chart(self) -> None:
        self.axes.clear()
        self.axes.set_title("Algorithm Comparison", fontsize=11)
        self.axes.set_ylabel("Visited Nodes")
        self.axes.set_facecolor("#fffdf8")
        if self.comparison_records:
            names = [item[0] for item in self.comparison_records]
            visited_values = [item[1] for item in self.comparison_records]
            colors = ["#2a9d8f", "#e9c46a", "#e76f51"][: len(names)]
            bars = self.axes.bar(names, visited_values, color=colors)
            for bar, record in zip(bars, self.comparison_records):
                self.axes.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, f"path {record[2]}", ha="center", va="bottom", fontsize=9)
        else:
            self.axes.text(0.5, 0.5, "Run a search to compare results", ha="center", va="center", transform=self.axes.transAxes)
        self.chart_canvas.draw()

    def draw_grid(self) -> None:
        self.canvas.delete("all")
        for row in range(self.solver.rows):
            for col in range(self.solver.cols):
                cell = (row, col)
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                fill = "#fffdf8"
                if cell in self.solver.obstacles:
                    fill = self.palette["wall"]
                elif cell in self.path_cells:
                    fill = self.palette["path"]
                elif cell in self.visited_cells:
                    fill = self.palette["visited"]
                if cell == self.solver.start:
                    fill = self.palette["start"]
                if cell == self.solver.goal:
                    fill = self.palette["goal"]

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=self.palette["grid"], width=2)
                if cell == self.solver.start:
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="S", fill="white", font=("Segoe UI", 12, "bold"))
                elif cell == self.solver.goal:
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="G", fill="white", font=("Segoe UI", 12, "bold"))


if __name__ == "__main__":
    app = DualGameSystem()
    app.mainloop()
