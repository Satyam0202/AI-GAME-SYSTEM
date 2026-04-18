# 🧠 AI-Based Dual Game System with Intelligent Decision Making

A comprehensive **modern web-based** application featuring two AI-powered games with intelligent algorithms for decision-making and pathfinding. Built with **Flask backend** and **HTML/CSS frontend**.

## 🎯 Overview

This project demonstrates practical applications of AI algorithms through interactive games:
- **Game AI**: Minimax algorithm with Alpha-Beta pruning
- **Search Algorithms**: A* pathfinding with optimal path finding
- **Modern Web UI**: Beautiful HTML/CSS responsive interface
- **Python Backend**: Flask API with AI algorithm implementation
- **Performance Metrics**: Real-time algorithm analysis and visualization

## 📋 Project Modules

### 🟢 Module 1: Tic Tac Toe - Minimax AI Game

A classic game where you play against an unbeatable AI opponent with modern web interface.

#### 🧠 Algorithm: Minimax with Alpha-Beta Pruning
- **Minimax**: Recursively evaluates all possible game states
- **Alpha-Beta Pruning**: Optimizes by eliminating unnecessary branches
- **Outcome**: AI always plays optimally

#### 🎯 Features
- Human vs AI gameplay with real-time interaction
- Algorithm statistics display
- Nodes evaluated counter
- Nodes pruned counter
- Win/Draw detection
- Responsive web interface

#### 💻 How to Play
1. Go to Tic Tac Toe game
2. Click on any empty cell to make your move (X)
3. AI responds automatically with its move (O)
4. Try to win - but the AI plays optimally!

---

### 🔵 Module 2: Maze Solver - A* Search Game

An interactive grid-based pathfinding game using HTML canvas visualization.

#### 🧠 Algorithm: A* Search Algorithm
- **A* Algorithm**: Combines actual cost (g) and estimated cost (h)
- **Heuristic**: Manhattan distance to goal
- **Efficiency**: Finds optimal path faster than BFS
- **Visualization**: Shows explored vs final path on canvas

#### 🎯 Features
- 10x10 grid-based maze with canvas rendering
- Pre-defined obstacles
- A* search visualization
- Path highlighting
- Algorithm statistics
- Real-time animation

#### 🎨 Grid Legend
- 🟢 **Green**: Start position (0,0)
- 🔴 **Red**: Goal position (9,9)
- 🟠 **Gray**: Obstacles
- 🔵 **Light Blue**: Visited nodes
- 🟡 **Yellow**: Final path

---

## 🛠️ Technologies Used

### Backend
- **Language**: Python 3.11+
- **Framework**: Flask
- **Data Structures**: Lists, Heaps, Dictionaries, Deques
- **Algorithms**: Minimax, Alpha-Beta Pruning, A*, BFS

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: Interactive gameplay
- **Canvas**: Maze visualization
- **Responsive Design**: Mobile-friendly interface

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone/Download the project**
   ```bash
   cd d:\ait
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Or manually:
   ```bash
   pip install Flask==2.3.2 Werkzeug==2.3.6
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

## 🚀 Quick Start

### Launch the Application
```bash
python app.py
```

The Flask server starts and you can access it at `http://localhost:5000`

### Main Menu
You'll see a beautiful landing page with two game options:
- 🎯 Tic Tac Toe (Minimax AI)
- 🗺️ Maze Solver (A* Search)

### Play Tic Tac Toe
1. Click "🎯 Tic Tac Toe" card
2. Click any empty cell to play X
3. AI plays O automatically
4. View algorithm statistics in real-time

### Solve Maze
1. Click "🗺️ Maze Solver" card
2. Click "🚀 Solve Maze" button
3. Watch the algorithm explore and find the path
4. See statistics: visited nodes and path length

## 📊 Algorithm Details

### Tic Tac Toe - Minimax Algorithm

**How it works:**
```
Minimax(position, depth, isMaximizing, alpha, beta):
    if terminal state:
        return evaluation
    
    if maximizing (AI's turn):
        maxEval = -∞
        for each move:
            eval = Minimax(..., False, alpha, beta)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha: break  // Pruning
        return maxEval
    else (human's turn):
        minEval = +∞
        for each move:
            eval = Minimax(..., True, alpha, beta)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha: break  // Pruning
        return minEval
```

**Board Evaluation:**
- +10: AI wins
- -10: Human wins
- 0: Draw

### Maze Solver - A* Algorithm

**How it works:**
```
A*(start, goal):
    openSet = priority queue with start node
    
    while openSet not empty:
        current = node with lowest f(n)
        
        if current == goal:
            return reconstruct_path(current)
        
        for each neighbor:
            newCost = cost[current] + 1
            if neighbor not in costMap or newCost < cost[neighbor]:
                cost[neighbor] = newCost
                f(neighbor) = g(neighbor) + h(neighbor)
                push to openSet
    
    return no path found
```

**Heuristic (Manhattan Distance):**
$$h(n) = |x_n - x_{goal}| + |y_n - y_{goal}|$$

## 📁 Project Structure

```
d:\ait\
├── app.py                      # Flask application & API endpoints
├── tic_tac_toe_ai.py          # Tic Tac Toe game with Minimax AI
├── maze_solver_ai.py          # Maze solver with A* algorithm
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
│
├── templates/
│   ├── index.html            # Main menu page
│   ├── tictactoe.html        # Tic Tac Toe game page
│   └── maze.html             # Maze solver game page
│
└── static/
    ├── css/
    │   └── style.css         # All CSS styling
    └── js/
        └── script.js         # JavaScript functionality
```

## 🎓 Learning Outcomes

After working with this project, you'll understand:

✅ **Game AI** - How AI makes optimal decisions  
✅ **Minimax Algorithm** - Game tree search and evaluation  
✅ **Alpha-Beta Pruning** - Optimization through branch elimination  
✅ **A* Pathfinding** - Optimal search with heuristics  
✅ **Heuristic Functions** - Estimating solution proximity  
✅ **Web Development** - Flask backend with REST APIs  
✅ **Frontend Design** - Modern HTML/CSS/JavaScript  
✅ **Canvas Rendering** - Graphics for visualization  
✅ **Performance Analysis** - Measuring algorithm efficiency  

## 🎨 UI/UX Features

✨ **Modern Design**
- Dark theme with neon green accents
- Smooth animations and transitions
- Gradient backgrounds and effects
- Responsive layout for all devices

🎯 **User Experience**
- Intuitive navigation
- Real-time feedback
- Clear algorithm statistics
- Beautiful visualizations

📱 **Responsive**
- Desktop optimized
- Tablet friendly
- Mobile responsive
- Works on all modern browsers

## 🔥 Key Features Highlighted

### Performance Metrics
- **Nodes Evaluated** (Tic Tac Toe): Game states analyzed by Minimax
- **Nodes Pruned**: Branches eliminated by Alpha-Beta pruning
- **Visited Nodes** (Maze): Cells explored during search
- **Path Length**: Steps to reach goal

### Real-time Interaction
- Instant move feedback
- Live algorithm statistics
- Smooth canvas animations
- Responsive button controls

### Visual Feedback
- Color-coded maze cells
- Game board highlighting
- Status messages
- Statistics dashboard

## 💡 Interesting Observations

1. **Tic Tac Toe AI**: If you play perfectly, you'll always draw
2. **Maze Solving**: A* explores fewer cells than BFS
3. **Heuristics Matter**: Manhattan distance works well for grids
4. **Pruning Power**: Alpha-Beta pruning can reduce search time by ~90%

## 🚀 Future Enhancements

### Possible Improvements
- [ ] Add difficulty levels for Tic Tac Toe
- [ ] Algorithm comparison (show BFS vs A*)
- [ ] Custom maze creation tool
- [ ] Multiplayer support
- [ ] Advanced statistics charts
- [ ] Move history and replay
- [ ] More games (Connect 4, Chess)
- [ ] Database for high scores
- [ ] Mobile app version
- [ ] Machine learning integration

## 📚 References & Resources

### Algorithms
- [Minimax Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Minimax)
- [Alpha-Beta Pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
- [A* Search Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)

### Web Technologies
- [Flask Documentation](https://flask.palletsprojects.com/)
- [HTML5 Canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
- [CSS Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations)

## 🎓 Project Strengths

✅ **Complete AI Curriculum**: Decision-making + Pathfinding  
✅ **Full Stack**: Backend algorithms + Frontend interface  
✅ **Modern Tech**: Flask + HTML/CSS/JavaScript  
✅ **Visual Learning**: Real-time algorithm visualization  
✅ **Production Ready**: Clean code and best practices  
✅ **Well-Documented**: Clear code with comments  
✅ **Extensible**: Easy to add more games/algorithms  
✅ **Interview Ready**: Great portfolio project  

## 🤝 Contributing

Feel free to:
- Add new games
- Implement new algorithms
- Improve UI/UX
- Optimize backend
- Fix any bugs
- Add new features

## 📝 License

This project is created for educational purposes.

## 🎯 Summary

This AI Game System is a **complete, modern, production-ready** application that combines:

- 🎮 **Game Development** - Interactive gameplay and UI
- 🧠 **Artificial Intelligence** - Advanced algorithms  
- 📊 **Algorithm Analysis** - Performance metrics
- 🎨 **Web Design** - Beautiful, responsive interface
- ⚙️ **Full Stack** - Backend and frontend integration

Perfect for learning, interviews, portfolios, and project presentations! 🚀

---

**Happy Gaming and Algorithm Learning!** 🎓✨

