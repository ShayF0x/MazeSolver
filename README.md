<div id="top"></div>
<h1 align="center">🧩 Maze & Graph Visualizer</h1>
<p align="center"><i>A Python application created for educational purposes to visualize and understand mazes and graphs through interactive algorithms and animations.</i></p>
<p align="center">
    <img src="https://img.shields.io/badge/build-Ready%20to%20go-brightgreen"/>
    <img src="https://img.shields.io/badge/dynamic/json?color=blue&label=Version&query=version&url=https%3A%2F%2Fraw.githubusercontent.com%2FShayF0x%2FMazeSolver%2Fmaster%2FMazeSolver.json"/>
    <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python"/>
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg"/>
</p>

![app image](/assets/images/app.png)

---

### 📚 Project Context
This project was developed as part of a university course aiming to demystify the concepts of mazes and graphs through interactive and visual tools. The goal was to create a pedagogical application that helps users understand:

- How mazes can be generated using algorithms
- How they can be modeled as graphs
- How different pathfinding algorithms behave in real time

The emphasis was on interactivity, clarity, and educational value, making the tool suitable for students, teachers, and anyone curious about graph theory and algorithmic thinking.

The project was designed from scratch in Python using Tkinter for the interface and Pillow for image processing in a special "museum mode".

By combining algorithm animation, graphical customization, and an intuitive user experience, the project serves both as a learning support and a playground for experimentation.

### Summary
- [📚 Project Context](#-project-context)
- [Summary](#summary)
- [🧠 What It Does](#-what-it-does)
- [🖥 Interface Overview](#-interface-overview)
- [🧩 Algorithms Explained](#-algorithms-explained)
  - [🏗 Maze Generation — Randomized Kruskal's Algorithm](#-maze-generation--randomized-kruskals-algorithm)
  - [🔎 Depth-First Search (DFS)](#-depth-first-search-dfs)
  - [🔍 Breadth-First Search (BFS)](#-breadth-first-search-bfs)
  - [🌟 A-Star Search (A\*)](#-a-star-search-a)
- [🎨 Museum Mode](#-museum-mode)
- [📦 Installation \& Requirements](#-installation--requirements)
- [📝 License](#-license)

<p align="right">(<a href="#top">back to top</a>)</p>

### 🧠 What It Does

This application allows you to:

- **Generate** mazes using the *Randomized Kruskal’s Algorithm*
- **Convert** the maze into a graph and visualize the connections between nodes
- **Solve** the maze using:
  - Depth-First Search (DFS)
  - Breadth-First Search (BFS)
  - A-Star (A*)
- **Customize** and interact with the maze:
  - Pause the animation
  - Draw your own walls manually
  - Speed up / slow down the animation
  - Switch to a *"Museum mode"* for a themed visualization (Joconde, marble walls, etc.)

<p align="right">(<a href="#top">back to top</a>)</p>

<br>

### 🖥 Interface Overview

- The maze is displayed as a grid.
- **Green cell** = Start  
- **Red cell** = End  
- **Black cells** = Walls  
- Use buttons on the left to select an algorithm or generate a maze.
- Use the right panel to convert to a graph or reset.
- Bottom-right has a delay slider and pause/play controls.

To exit or change display modes, go to **Settings** → `Exit` or `Modes`.

<p align="right">(<a href="#top">back to top</a>)</p>

<br>

### 🧩 Algorithms Explained

#### [🏗 Maze Generation — Randomized Kruskal's Algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)

This method starts with all cells as walls and connects them step by step using a randomized union of cells that doesn't form cycles, creating a perfect maze (one path between any two points).

#### [🔎 Depth-First Search (DFS)](https://en.wikipedia.org/wiki/Depth-first_search)

DFS explores as far as possible along one branch before backtracking. This results in a very "depth-oriented" path, which may not be the shortest.

- Stack-based approach
- Not optimal (may not find shortest path)
- Fast and intuitive

#### [🔍 Breadth-First Search (BFS)](https://en.wikipedia.org/wiki/Breadth-first_search)

BFS explores all neighbors at the current depth before going deeper. It guarantees the shortest path in an unweighted graph.

- Queue-based
- Guarantees optimal path
- Slower than DFS in wide graphs

#### [🌟 A-Star Search (A*)](https://en.wikipedia.org/wiki/A*_search_algorithm)

A* uses a heuristic to prioritize paths that are likely to lead to the goal quickly. It’s the fastest and most efficient for many cases.

- Uses `f(n) = g(n) + h(n)`:
  - `g(n)` = cost from start to current
  - `h(n)` = estimated cost to goal (Manhattan distance)
- Optimal and efficient

Each algorithm is visualized **step by step**, so you can see it in action!

<p align="right">(<a href="#top">back to top</a>)</p>

<br>

### 🎨 Museum Mode

Activate a themed view:

- Start cell becomes a **Mona Lisa**
- End cell becomes a **museum door**
- Walls look like **dark marble blocks**
- Paths are replaced with **museum floor tiles**

<p align="right">(<a href="#top">back to top</a>)</p>

<br>

### 📦 Installation & Requirements

This project uses Python and relies on:

- `tkinter`
- `Pillow`

Install dependencies with:

```bash
pip install -r requirements.txt
```

Then run the app with:

```bash
python src/app.py
```

> Recommended for Python 3.10+

<p align="right">(<a href="#top">back to top</a>)</p>

### 📝 License

This project is under the [MIT](https://choosealicense.com/licenses/mit/) License.
<p align="right">(<a href="#top">back to top</a>)</p>
