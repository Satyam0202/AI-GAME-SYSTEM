"""
AI-Based Dual Game System with Intelligent Decision Making
Main Application with Menu System
"""

import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path

# Import game modules
from tic_tac_toe_ai import TicTacToeGame
from maze_solver_ai import MazeSolverGame


class MainMenu:
    """Main Menu Interface for Game Selection"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI Game System - Main Menu")
        self.root.geometry("600x400")
        self.root.configure(bg="#1a1a1a")
        
        # Style
        self.bg_color = "#1a1a1a"
        self.fg_color = "#00ff00"
        self.button_bg = "#003300"
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup main menu UI"""
        # Title
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=30)
        
        title = tk.Label(
            title_frame,
            text="🧠 AI-Based Game System 🎮",
            font=("Arial", 24, "bold"),
            fg=self.fg_color,
            bg=self.bg_color
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Intelligent Decision Making & Path Finding",
            font=("Arial", 12),
            fg="#00aa00",
            bg=self.bg_color
        )
        subtitle.pack()
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20, expand=True)
        
        # Tic Tac Toe Button
        ttt_btn = tk.Button(
            button_frame,
            text="🎯 Tic Tac Toe\n(Minimax AI)",
            font=("Arial", 14, "bold"),
            bg=self.button_bg,
            fg=self.fg_color,
            width=20,
            height=3,
            command=self.play_tic_tac_toe,
            relief=tk.RAISED,
            bd=2
        )
        ttt_btn.pack(pady=15)
        
        # Maze Solver Button
        maze_btn = tk.Button(
            button_frame,
            text="🗺️ Maze Solver\n(A* Search Algorithm)",
            font=("Arial", 14, "bold"),
            bg=self.button_bg,
            fg=self.fg_color,
            width=20,
            height=3,
            command=self.play_maze_solver,
            relief=tk.RAISED,
            bd=2
        )
        maze_btn.pack(pady=15)
        
        # Info Frame
        info_frame = tk.Frame(self.root, bg="#002200")
        info_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        info_text = tk.Label(
            info_frame,
            text="🔥 Features: AI Decision Making | Search Algorithms | Path Visualization | Performance Metrics",
            font=("Arial", 9),
            fg="#00dd00",
            bg="#002200"
        )
        info_text.pack(pady=10)
    
    def play_tic_tac_toe(self):
        """Launch Tic Tac Toe Game"""
        self.root.withdraw()
        game_window = tk.Toplevel(self.root)
        game = TicTacToeGame(game_window, self.root)
    
    def play_maze_solver(self):
        """Launch Maze Solver Game"""
        self.root.withdraw()
        game_window = tk.Toplevel(self.root)
        game = MazeSolverGame(game_window, self.root)


def main():
    """Main Entry Point"""
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
