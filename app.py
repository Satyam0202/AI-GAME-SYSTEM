"""
Flask Application - AI Game System Backend
HTML/CSS Frontend with Python Backend
"""

from flask import Flask, render_template, request, jsonify
from tic_tac_toe_ai import TicTacToeAI, Player
from maze_solver_ai import MazeSolver
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Game instances
tictactoe_ai = TicTacToeAI()
maze_solver = MazeSolver(10, 10)


@app.route('/')
def index():
    """Main menu page"""
    return render_template('index.html')


@app.route('/tictactoe')
def tictactoe():
    """Tic Tac Toe game page"""
    return render_template('tictactoe.html')


@app.route('/maze')
def maze():
    """Maze Solver game page"""
    return render_template('maze.html')


# ==================== TIC TAC TOE ENDPOINTS ====================

@app.route('/api/tictactoe/init', methods=['POST'])
def init_tictactoe():
    """Initialize a new Tic Tac Toe game"""
    global tictactoe_ai
    tictactoe_ai = TicTacToeAI()
    return jsonify({
        'status': 'success',
        'board': [[Player.EMPTY.value for _ in range(3)] for _ in range(3)]
    })


@app.route('/api/tictactoe/move', methods=['POST'])
def tictactoe_move():
    """Handle Tic Tac Toe move"""
    data = request.json
    board = data.get('board')
    row = data.get('row')
    col = data.get('col')
    
    # Convert to list of lists if needed
    if isinstance(board, list):
        board = [list(r) if isinstance(r, list) else r for r in board]
    
    # Human move
    board[row][col] = Player.HUMAN.value
    
    # Check if human won
    score = tictactoe_ai.evaluate(board)
    if score == -10:
        return jsonify({
            'status': 'human_won',
            'board': board,
            'message': 'You Won! 🎉'
        })
    
    # Check for draw
    if tictactoe_ai.is_terminal(board):
        return jsonify({
            'status': 'draw',
            'board': board,
            'message': 'Draw! 🤝'
        })
    
    # AI move
    ai_move = tictactoe_ai.find_best_move(board)
    
    if ai_move:
        row, col = ai_move
        board[row][col] = Player.AI.value
        
        # Check if AI won
        score = tictactoe_ai.evaluate(board)
        if score == 10:
            return jsonify({
                'status': 'ai_won',
                'board': board,
                'ai_move': ai_move,
                'stats': {
                    'nodes_evaluated': tictactoe_ai.nodes_evaluated,
                    'nodes_pruned': tictactoe_ai.pruned_nodes
                },
                'message': 'AI Won! 🤖'
            })
        
        # Check for draw
        if tictactoe_ai.is_terminal(board):
            return jsonify({
                'status': 'draw',
                'board': board,
                'ai_move': ai_move,
                'stats': {
                    'nodes_evaluated': tictactoe_ai.nodes_evaluated,
                    'nodes_pruned': tictactoe_ai.pruned_nodes
                },
                'message': 'Draw! 🤝'
            })
        
        return jsonify({
            'status': 'success',
            'board': board,
            'ai_move': ai_move,
            'stats': {
                'nodes_evaluated': tictactoe_ai.nodes_evaluated,
                'nodes_pruned': tictactoe_ai.pruned_nodes
            }
        })
    
    return jsonify({
        'status': 'error',
        'message': 'Error in AI move'
    })


# ==================== MAZE ENDPOINTS ====================

@app.route('/api/maze/init', methods=['POST'])
def init_maze():
    """Initialize a new maze"""
    global maze_solver
    maze_solver = MazeSolver(10, 10)
    
    maze_data = {
        'start': maze_solver.start,
        'goal': maze_solver.goal,
        'obstacles': list(maze_solver.obstacles),
        'grid_size': maze_solver.rows
    }
    
    return jsonify({
        'status': 'success',
        'maze': maze_data
    })


@app.route('/api/maze/solve', methods=['POST'])
def solve_maze():
    """Solve the maze using A*"""
    data = request.json
    algorithm = data.get('algorithm', 'A*')
    
    path, visited, stats = maze_solver.solve(algorithm)
    
    return jsonify({
        'status': 'success',
        'path': path,
        'visited': visited,
        'stats': {
            'algorithm': stats.algorithm,
            'found': stats.found,
            'visited_nodes': stats.visited_nodes,
            'path_length': stats.path_length
        }
    })


@app.route('/api/maze/data', methods=['GET'])
def get_maze_data():
    """Get current maze data"""
    maze_data = {
        'start': maze_solver.start,
        'goal': maze_solver.goal,
        'obstacles': list(maze_solver.obstacles),
        'grid_size': maze_solver.rows
    }
    
    return jsonify({
        'status': 'success',
        'maze': maze_data
    })


if __name__ == '__main__':
    print("🧠 AI Game System Server Starting...")
    print("🌐 Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
