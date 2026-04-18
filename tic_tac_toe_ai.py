"""
Tic Tac Toe Game with AI using Minimax Algorithm with Alpha-Beta Pruning
"""

import tkinter as tk
from tkinter import messagebox
import time
from enum import Enum
from dataclasses import dataclass


class Player(Enum):
    """Player enumeration"""
    HUMAN = 1
    AI = -1
    EMPTY = 0


@dataclass
class MoveStats:
    """Statistics for AI move"""
    algorithm: str
    explored_nodes: int
    score: int


class TicTacToeAI:
    """Minimax AI for Tic Tac Toe with Alpha-Beta Pruning"""
    
    def __init__(self):
        self.nodes_evaluated = 0
        self.pruned_nodes = 0
    
    def new_board(self):
        """Create a new empty board (1D representation: 9 elements)"""
        return [0] * 9
    
    def _flat_to_2d(self, flat_board):
        """Convert 1D board to 2D board"""
        return [flat_board[i*3:(i+1)*3] for i in range(3)]
    
    def _2d_to_flat(self, board_2d):
        """Convert 2D board to 1D board"""
        flat = []
        for row in board_2d:
            flat.extend(row)
        return flat
    
    def check_winner(self, flat_board):
        """Check for winner in 1D board. Returns 'X', 'O', 'Draw', or None"""
        board = self._flat_to_2d(flat_board)
        
        # Check rows
        for row in board:
            if all(cell == 1 for cell in row):  # X is all 1s
                return "X"
            if all(cell == -1 for cell in row):  # O is all -1s
                return "O"
        
        # Check columns
        for col in range(3):
            if all(board[row][col] == 1 for row in range(3)):
                return "X"
            if all(board[row][col] == -1 for row in range(3)):
                return "O"
        
        # Check diagonals
        if all(board[i][i] == 1 for i in range(3)):
            return "X"
        if all(board[i][i] == -1 for i in range(3)):
            return "O"
        
        if all(board[i][2-i] == 1 for i in range(3)):
            return "X"
        if all(board[i][2-i] == -1 for i in range(3)):
            return "O"
        
        # Check for draw
        if all(cell != 0 for cell in flat_board):
            return "Draw"
        
        return None
    
    def best_move(self, flat_board, algorithm="Alpha-Beta"):
        """Find best move for AI. Returns (move_index, stats) tuple"""
        board = self._flat_to_2d(flat_board)
        self.nodes_evaluated = 0
        self.pruned_nodes = 0
        
        best_score = float('-inf')
        best_move = None
        empty_cells = self.get_empty_cells(board)
        
        for i, j in empty_cells:
            board[i][j] = Player.AI.value
            if algorithm == "Minimax":
                score = self.minimax(board, 0, False, float('-inf'), float('inf'))
            else:  # Alpha-Beta (default)
                score = self.minimax(board, 0, False, float('-inf'), float('inf'))
            board[i][j] = Player.EMPTY.value
            
            if score > best_score:
                best_score = score
                best_move = i * 3 + j  # Convert 2D to 1D index
        
        stats = MoveStats(algorithm=algorithm, explored_nodes=self.nodes_evaluated, score=best_score)
        return best_move, stats
    
    def evaluate(self, board):
        """
        Evaluate board position
        +10: AI wins
        -10: Human wins
        0: Draw
        """
        # Check rows
        for row in board:
            if all(cell == Player.AI.value for cell in row):
                return 10
            if all(cell == Player.HUMAN.value for cell in row):
                return -10
        
        # Check columns
        for col in range(3):
            if all(board[row][col] == Player.AI.value for row in range(3)):
                return 10
            if all(board[row][col] == Player.HUMAN.value for row in range(3)):
                return -10
        
        # Check diagonals
        if all(board[i][i] == Player.AI.value for i in range(3)):
            return 10
        if all(board[i][i] == Player.HUMAN.value for i in range(3)):
            return -10
        
        if all(board[i][2-i] == Player.AI.value for i in range(3)):
            return 10
        if all(board[i][2-i] == Player.HUMAN.value for i in range(3)):
            return -10
        
        return 0
    
    def is_terminal(self, board):
        """Check if game is over"""
        # Check for winner
        if self.evaluate(board) != 0:
            return True
        
        # Check if board is full
        for row in board:
            if any(cell == Player.EMPTY.value for cell in row):
                return False
        return True
    
    def get_empty_cells(self, board):
        """Get list of empty cells"""
        empty = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == Player.EMPTY.value:
                    empty.append((i, j))
        return empty
    
    def minimax(self, board, depth, is_maximizing, alpha, beta):
        """
        Minimax with Alpha-Beta Pruning
        """
        self.nodes_evaluated += 1
        
        score = self.evaluate(board)
        
        # Terminal node
        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if self.is_terminal(board):
            return 0
        
        empty_cells = self.get_empty_cells(board)
        
        if is_maximizing:  # AI's turn
            max_eval = float('-inf')
            for i, j in empty_cells:
                board[i][j] = Player.AI.value
                eval = self.minimax(board, depth + 1, False, alpha, beta)
                board[i][j] = Player.EMPTY.value
                
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    self.pruned_nodes += 1
                    break
            
            return max_eval
        else:  # Human's turn
            min_eval = float('inf')
            for i, j in empty_cells:
                board[i][j] = Player.HUMAN.value
                eval = self.minimax(board, depth + 1, True, alpha, beta)
                board[i][j] = Player.EMPTY.value
                
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    self.pruned_nodes += 1
                    break
            
            return min_eval
    
    def find_best_move(self, board):
        """Find best move for AI"""
        self.nodes_evaluated = 0
        self.pruned_nodes = 0
        
        best_score = float('-inf')
        best_move = None
        empty_cells = self.get_empty_cells(board)
        
        for i, j in empty_cells:
            board[i][j] = Player.AI.value
            score = self.minimax(board, 0, False, float('-inf'), float('inf'))
            board[i][j] = Player.EMPTY.value
            
            if score > best_score:
                best_score = score
                best_move = (i, j)
        
        return best_move


class TicTacToeGame:
    """Tic Tac Toe Game UI and Logic"""
    
    def __init__(self, game_window, parent_window):
        self.game_window = game_window
        self.parent_window = parent_window
        self.game_window.title("Tic Tac Toe - AI Game")
        self.game_window.geometry("600x700")
        self.game_window.configure(bg="#1a1a1a")
        
        # Game variables
        self.board = [[Player.EMPTY.value for _ in range(3)] for _ in range(3)]
        self.ai = TicTacToeAI()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.human_first = True
        
        self.setup_ui()
        self.game_window.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_ui(self):
        """Setup game UI"""
        # Title
        title = tk.Label(
            self.game_window,
            text="🎯 Tic Tac Toe - Minimax AI",
            font=("Arial", 18, "bold"),
            fg="#00ff00",
            bg="#1a1a1a"
        )
        title.pack(pady=10)
        
        # Info
        info = tk.Label(
            self.game_window,
            text="You are X | AI is O",
            font=("Arial", 12),
            fg="#00aa00",
            bg="#1a1a1a"
        )
        info.pack()
        
        # Game Board
        board_frame = tk.Frame(self.game_window, bg="#1a1a1a")
        board_frame.pack(pady=20)
        
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 20, "bold"),
                    width=5,
                    height=2,
                    bg="#003300",
                    fg="#00ff00",
                    command=lambda row=i, col=j: self.human_move(row, col)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn
        
        # Stats Frame
        stats_frame = tk.Frame(self.game_window, bg="#002200")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Game Statistics:\nNodes Evaluated: 0 | Nodes Pruned: 0",
            font=("Arial", 10),
            fg="#00dd00",
            bg="#002200",
            justify=tk.LEFT
        )
        self.stats_label.pack(pady=10)
        
        # Control Frame
        control_frame = tk.Frame(self.game_window, bg="#1a1a1a")
        control_frame.pack(pady=10)
        
        reset_btn = tk.Button(
            control_frame,
            text="🔄 New Game",
            font=("Arial", 12, "bold"),
            bg="#003300",
            fg="#00ff00",
            command=self.reset_game
        )
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = tk.Button(
            control_frame,
            text="🏠 Back to Menu",
            font=("Arial", 12, "bold"),
            bg="#003300",
            fg="#00ff00",
            command=self.on_close
        )
        back_btn.pack(side=tk.LEFT, padx=10)
    
    def human_move(self, row, col):
        """Handle human player move"""
        if self.game_over or self.board[row][col] != Player.EMPTY.value:
            return
        
        # Human move
        self.board[row][col] = Player.HUMAN.value
        self.update_button(row, col, "X", "#ff0000")
        
        # Check if human won
        if self.check_winner():
            messagebox.showinfo("Game Over", "You Won! 🎉")
            self.game_over = True
            return
        
        # Check for draw
        if self.is_board_full():
            messagebox.showinfo("Game Over", "It's a Draw! 🤝")
            self.game_over = True
            return
        
        # AI move
        self.game_window.after(500, self.ai_move)
    
    def ai_move(self):
        """Handle AI move"""
        if self.game_over:
            return
        
        move = self.ai.find_best_move(self.board)
        
        if move:
            row, col = move
            self.board[row][col] = Player.AI.value
            self.update_button(row, col, "O", "#0000ff")
            
            # Update stats
            self.stats_label.config(
                text=f"Game Statistics:\nNodes Evaluated: {self.ai.nodes_evaluated} | Nodes Pruned: {self.ai.pruned_nodes}"
            )
            
            # Check if AI won
            if self.check_winner():
                messagebox.showinfo("Game Over", "AI Won! 🤖")
                self.game_over = True
                return
            
            # Check for draw
            if self.is_board_full():
                messagebox.showinfo("Game Over", "It's a Draw! 🤝")
                self.game_over = True
                return
    
    def update_button(self, row, col, symbol, color):
        """Update button display"""
        self.buttons[row][col].config(text=symbol, fg=color)
        self.buttons[row][col].config(state=tk.DISABLED)
    
    def check_winner(self):
        """Check if there's a winner"""
        score = self.ai.evaluate(self.board)
        return score != 0
    
    def is_board_full(self):
        """Check if board is full"""
        for row in self.board:
            if any(cell == Player.EMPTY.value for cell in row):
                return False
        return True
    
    def reset_game(self):
        """Reset the game"""
        self.board = [[Player.EMPTY.value for _ in range(3)] for _ in range(3)]
        self.game_over = False
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", fg="#00ff00", state=tk.NORMAL)
        
        self.stats_label.config(
            text="Game Statistics:\nNodes Evaluated: 0 | Nodes Pruned: 0"
        )
    
    def on_close(self):
        """Close the game window"""
        self.game_window.destroy()
        self.parent_window.deiconify()
