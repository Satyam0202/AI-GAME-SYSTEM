# ALL PROJECT NOTES

## 1. Project Summary

This project is an AI game system built around two main ideas:

- Tic Tac Toe with Minimax + Alpha-Beta pruning
- Maze solving with A*, BFS, and Hill Climbing
- Flask based web app with HTML/CSS/JS frontend
- Tkinter based desktop versions also present in the repo

In short, this repo has both:

- a web version: `app.py` + `templates/` + `static/`
- desktop versions: `main.py` and `dual_game_system.py`

## 2. Main Run Commands

### Web app

```bash
pip install -r requirements.txt
python app.py
```

Open:

```text
http://localhost:5000
```

### Desktop app (basic)

```bash
python main.py
```

### Desktop app (better UI + comparison chart)

```bash
python dual_game_system.py
```

Note:

- `dual_game_system.py` uses `matplotlib`
- `requirements.txt` currently contains only Flask and Werkzeug

## 3. Repo Structure

```text
D:\ait
|-- app.py
|-- dual_game_system.py
|-- main.py
|-- maze_solver_ai.py
|-- README.md
|-- requirements.txt
|-- tic_tac_toe_ai.py
|-- templates
|   |-- index.html
|   |-- maze.html
|   `-- tictactoe.html
|-- static
|   |-- css
|   |   `-- style.css
|   `-- js
|       `-- script.js
|-- .venv
`-- __pycache__
```

Important:

- `.venv/` is local environment data
- `__pycache__/` is generated cache
- core project source is the Python, HTML, CSS, JS, and Markdown files listed above

## 4. What Each File Does

### `app.py`

Main Flask backend. It:

- serves the home page
- serves Tic Tac Toe page
- serves Maze page
- exposes Tic Tac Toe APIs
- exposes Maze APIs

Key routes:

- `/`
- `/tictactoe`
- `/maze`
- `/api/tictactoe/init`
- `/api/tictactoe/move`
- `/api/maze/init`
- `/api/maze/solve`
- `/api/maze/data`

### `tic_tac_toe_ai.py`

Main Tic Tac Toe logic file. It contains:

- `Player` enum
- `MoveStats` dataclass
- `TicTacToeAI`
- old Tkinter based `TicTacToeGame`

Important logic:

- board evaluation
- winner detection
- empty-cell search
- Minimax recursion
- Alpha-Beta pruning counters

### `maze_solver_ai.py`

Main maze logic file. It contains:

- `MazeStats` dataclass
- `MazeSolver`
- old Tkinter based `MazeSolverGame`

Important logic:

- random obstacle generation
- BFS
- A*
- Hill Climbing
- path reconstruction

### `dual_game_system.py`

This is the more polished desktop app. It includes:

- home screen
- Tic Tac Toe desktop page
- Maze page
- algorithm selection
- animated grid updates
- matplotlib comparison chart

### `main.py`

Older/simple Tkinter menu launcher. It opens:

- `TicTacToeGame`
- `MazeSolverGame`

### `templates/index.html`

Landing page for the web app with cards for both modules.

### `templates/tictactoe.html`

Web Tic Tac Toe page. Includes:

- board UI
- AI mode
- two-player mode
- frontend JS logic inside the same HTML file

### `templates/maze.html`

Web Maze page. Includes:

- canvas-based maze drawing
- Solve / Reset buttons
- stats display
- frontend JS logic inside the same HTML file

### `static/css/style.css`

Global styling:

- dark neon theme
- cards
- buttons
- board
- canvas styles
- legends
- stats panels
- responsive layout

### `static/js/script.js`

Small shared JS file for:

- smooth scrolling
- button click visual feedback
- basic page-load logs

### `README.md`

Long-form project documentation covering:

- project overview
- module explanation
- algorithms
- install steps
- learning outcomes
- possible future improvements

### `requirements.txt`

Current dependencies:

```text
Flask==2.3.2
Werkzeug==2.3.6
```

## 5. Real Project Flow

### Web flow

1. User opens `/`
2. Flask renders `templates/index.html`
3. User chooses Tic Tac Toe or Maze
4. Frontend uses `fetch(...)` to call Flask APIs
5. Flask calls algorithm classes from Python files
6. JSON response comes back
7. UI updates board/canvas/stats

### Desktop flow

1. User runs `main.py` or `dual_game_system.py`
2. Tkinter UI opens
3. Buttons navigate between screens
4. Python algorithm classes run locally
5. UI updates directly without web APIs

## 6. Important Backend Code

### `app.py` route setup

```python
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tictactoe')
def tictactoe():
    return render_template('tictactoe.html')

@app.route('/maze')
def maze():
    return render_template('maze.html')
```

### `app.py` Tic Tac Toe API

```python
@app.route('/api/tictactoe/move', methods=['POST'])
def tictactoe_move():
    data = request.json
    board = data.get('board')
    row = data.get('row')
    col = data.get('col')

    board[row][col] = Player.HUMAN.value

    score = tictactoe_ai.evaluate(board)
    if score == -10:
        return jsonify({'status': 'human_won', 'board': board})

    if tictactoe_ai.is_terminal(board):
        return jsonify({'status': 'draw', 'board': board})

    ai_move = tictactoe_ai.find_best_move(board)
    if ai_move:
        row, col = ai_move
        board[row][col] = Player.AI.value

    return jsonify({
        'status': 'success',
        'board': board,
        'ai_move': ai_move,
        'stats': {
            'nodes_evaluated': tictactoe_ai.nodes_evaluated,
            'nodes_pruned': tictactoe_ai.pruned_nodes
        }
    })
```

### `app.py` Maze API

```python
@app.route('/api/maze/solve', methods=['POST'])
def solve_maze():
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
```

## 7. Important Tic Tac Toe Code

### Core AI classes

```python
class Player(Enum):
    HUMAN = 1
    AI = -1
    EMPTY = 0

@dataclass
class MoveStats:
    algorithm: str
    explored_nodes: int
    score: int
```

### Board evaluation

```python
def evaluate(self, board):
    for row in board:
        if all(cell == Player.AI.value for cell in row):
            return 10
        if all(cell == Player.HUMAN.value for cell in row):
            return -10

    for col in range(3):
        if all(board[row][col] == Player.AI.value for row in range(3)):
            return 10
        if all(board[row][col] == Player.HUMAN.value for row in range(3)):
            return -10

    if all(board[i][i] == Player.AI.value for i in range(3)):
        return 10
    if all(board[i][i] == Player.HUMAN.value for i in range(3)):
        return -10

    if all(board[i][2-i] == Player.AI.value for i in range(3)):
        return 10
    if all(board[i][2-i] == Player.HUMAN.value for i in range(3)):
        return -10

    return 0
```

### Minimax with Alpha-Beta pruning

```python
def minimax(self, board, depth, is_maximizing, alpha, beta):
    self.nodes_evaluated += 1

    score = self.evaluate(board)
    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if self.is_terminal(board):
        return 0

    empty_cells = self.get_empty_cells(board)

    if is_maximizing:
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
    else:
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
```

### Best move search

```python
def find_best_move(self, board):
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
```

## 8. Important Maze Solver Code

### Solver entry

```python
def solve(self, algorithm: str):
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
```

### Neighbor generation + heuristic

```python
def neighbors(self, cell):
    row, col = cell
    for next_row, next_col in (
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ):
        next_cell = (next_row, next_col)
        if 0 <= next_row < self.rows and 0 <= next_col < self.cols and next_cell not in self.obstacles:
            yield next_cell

def heuristic(self, cell):
    return abs(cell[0] - self.goal[0]) + abs(cell[1] - self.goal[1])
```

### BFS

```python
def _bfs(self):
    queue = deque([self.start])
    parent = {self.start: None}
    visited_order = []
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
```

### A*

```python
def _astar(self):
    heap = [(self.heuristic(self.start), 0, self.start)]
    parent = {self.start: None}
    cost_so_far = {self.start: 0}
    visited_order = []
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
```

### Hill Climbing

```python
def _hill_climbing(self):
    current = self.start
    parent = {self.start: None}
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
```

## 9. Important Frontend Code

### `templates/index.html`

Main landing page highlights:

- one card for Tic Tac Toe
- one card for Maze Solver
- both cards directly link to Flask routes

Core structure:

```html
<a href="/tictactoe" class="game-card tictactoe-card">...</a>
<a href="/maze" class="game-card maze-card">...</a>
```

### `templates/tictactoe.html`

This page contains both UI and game logic in the same file.

Important state:

```javascript
let gameBoard = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
let gameOver = false;
let gameMode = 'AI';
let currentPlayer = 1;
```

Important frontend move handling:

```javascript
function handleMove(row, col) {
    if (gameOver || gameBoard[row][col] !== 0) return;

    if (gameMode === 'AI') {
        makeAIMove(row, col);
    } else {
        makeHumanMove(row, col);
    }
}
```

Important API call:

```javascript
function makeAIMove(row, col) {
    fetch('/api/tictactoe/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board: gameBoard, row: row, col: col })
    })
    .then(res => res.json())
    .then(data => {
        gameBoard = data.board;
        drawBoard();

        if (data.stats) {
            document.getElementById('nodesEvaluated').textContent = data.stats.nodes_evaluated;
            document.getElementById('nodesPruned').textContent = data.stats.nodes_pruned;
        }
    });
}
```

### `templates/maze.html`

Important frontend state:

```javascript
const canvas = document.getElementById('mazeCanvas');
const ctx = canvas.getContext('2d');
const GRID_SIZE = 10;
const CELL_SIZE = 50;

let maze = null;
let path = [];
let visited = [];
let solving = false;
```

Maze load flow:

```javascript
function loadMaze() {
    fetch('/api/maze/init', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            maze = data.maze;
            path = [];
            visited = [];
            drawMaze();
        });
}
```

Maze solve flow:

```javascript
function solveMaze() {
    if (solving || !maze) return;
    solving = true;

    fetch('/api/maze/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ algorithm: 'A*' })
    })
    .then(res => res.json())
    .then(data => {
        const stats = data.stats;
        path = stats.found ? data.path : [];
        visited = data.visited;
        drawMaze();
    });
}
```

### `static/js/script.js`

Shared JS:

```javascript
document.querySelectorAll('.btn, .play-btn').forEach(button => {
    button.addEventListener('click', function() {
        if (!this.classList.contains('no-loading')) {
            this.style.opacity = '0.7';
            setTimeout(() => {
                this.style.opacity = '1';
            }, 200);
        }
    });
});
```

### `static/css/style.css`

Theme variables:

```css
:root {
    --primary-color: #00ff00;
    --primary-dark: #003300;
    --secondary-color: #0088ff;
    --bg-dark: #1a1a1a;
    --bg-darker: #0d0d0d;
    --text-light: #00dd00;
    --accent-danger: #ff0000;
    --accent-warning: #ffff00;
}
```

Important UI sections covered in CSS:

- menu page
- game page
- Tic Tac Toe board
- maze canvas
- stats panels
- responsive rules for tablet/mobile

## 10. Desktop App Notes

### `main.py`

Simple Tkinter launcher:

```python
def main():
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()
```

It opens:

- `TicTacToeGame` from `tic_tac_toe_ai.py`
- `MazeSolverGame` from `maze_solver_ai.py`

### `dual_game_system.py`

This is a cleaner desktop version. It adds:

- multi-page layout inside one Tk app
- algorithm choice for Tic Tac Toe
- BFS / A* / Hill Climbing comparison
- obstacle toggling on grid
- animated exploration
- bar chart for visited-node comparison

Important setup:

```python
for frame_class in (HomePage, TicTacToePage, MazeSolverPage):
    frame = frame_class(container, self)
    self.frames[frame_class.__name__] = frame
    frame.grid(row=0, column=0, sticky="nsew")
```

Important maze comparison update:

```python
def _record_comparison(self, algorithm: str, visited_nodes: int, path_length: int) -> None:
    self.comparison_records = [record for record in self.comparison_records if record[0] != algorithm]
    self.comparison_records.append((algorithm, visited_nodes, path_length))
    self.comparison_records.sort(key=lambda item: item[0])
    self.refresh_chart()
```

## 11. README Key Points

`README.md` already covers these areas:

- overview of both modules
- Minimax explanation
- A* explanation
- install guide
- project structure
- learning outcomes
- UI features
- future enhancement ideas

If someone wants project presentation material, README + this file together are enough for a quick walkthrough.

## 12. Important Observations

### Good parts

- clean separation between backend logic and frontend display in web version
- reusable algorithm classes
- both web and desktop interfaces exist
- stats are exposed in both game modules

### Notable details

- web Tic Tac Toe page supports two-player mode in frontend only
- AI mode uses Flask backend
- web Maze page currently calls only A* even though backend solver supports BFS and Hill Climbing
- `dual_game_system.py` is more feature-rich than the Flask frontend in some places

### Dependency gap

- `dual_game_system.py` imports `matplotlib`
- `requirements.txt` does not include `matplotlib`

## 13. Best Files To Study First

If someone wants to understand the project fast, read in this order:

1. `README.md`
2. `app.py`
3. `tic_tac_toe_ai.py`
4. `maze_solver_ai.py`
5. `templates/tictactoe.html`
6. `templates/maze.html`
7. `static/css/style.css`
8. `dual_game_system.py`

## 14. Final One-Line Understanding

This repo is an AI learning project that combines game decision-making and pathfinding, implemented in Python, exposed through Flask for the web, and also available in Tkinter desktop form with extra comparison features.
