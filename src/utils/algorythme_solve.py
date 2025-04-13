from utils.tkinter_process import *
from tkinter import *
from widget.cell import Cell, CellType, CellState, CELL_SIZE
from collections import deque
from heapq import heappop, heappush
from math import *
from model.model import Model

NORTH, EAST, SOUTH, WEST = (0, -1), (1, 0), (0, 1), (-1, 0)

def is_valid_move(cells: dict[tuple[int, int], Cell], position: int):
    return position in cells and (cells[position].state == CellState.EMPTY or cells[position].cellType == CellType.END)

def start_dfs(cells: dict[tuple[int, int], Cell], model: Model):
    index = 0
    start = (0,0)
    for cell in cells.values():
        if cell.cellType == CellType.BEGIN:
            start = cell.location

    stack = [start]
    visited = set()
    current = start

    while stack:
        if(model.on_pause.get()):
            tkpause(model.on_pause)

        cells[current].create_circle(CELL_SIZE/2, CELL_SIZE/2, CELL_SIZE/3, fill="#ff6352", outline="#ff6352", tags='alg')
        cells[current].create_text(CELL_SIZE/2, CELL_SIZE/2-1, fill="#000", text=f"{index}", tags='alg')
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        cells[current].create_circle(CELL_SIZE/2, CELL_SIZE/2, CELL_SIZE/3, fill="#697ef5", outline="#697ef5", tags='alg')  # Blue for visited
        tksleep(0.1*model.speed_var.get())

        if cells[current].cellType == CellType.END:
            break

        for direction in [NORTH, EAST, SOUTH, WEST]:
            next_cell = (current[0] + direction[0], current[1] + direction[1])
            if is_valid_move(cells, next_cell) and next_cell not in visited:
                stack.append(next_cell)
        
        index+=1


def start_bfs(cells, model: Model):
    index = 0
    start = (0,0)
    for cell in cells.values():
        if cell.cellType == CellType.BEGIN:
            start = cell.location

    queue = deque([start])
    visited = set()
    parent = {start: None}
    current = start

    while queue:
        if(model.on_pause.get()):
            tkpause(model.on_pause)

        cells[current].create_circle(CELL_SIZE/2, CELL_SIZE/2, CELL_SIZE/3, fill="#ff6352", outline="#ff6352", tags='alg')
        cells[current].create_text(CELL_SIZE/2, CELL_SIZE/2-1, fill="#000", text=f"{index}", tags='alg')
        current = queue.popleft()
        if current in visited:
            continue

        visited.add(current)
        cells[current].create_circle(CELL_SIZE/2, CELL_SIZE/2, CELL_SIZE/3, fill="#697ef5", outline="#697ef5", tags='alg')  # Blue for visited
        tksleep(0.1*model.speed_var.get())

        if cells[current].cellType == CellType.END:
            break

        for direction in [NORTH, EAST, SOUTH, WEST]:
            next_cell = (current[0] + direction[0], current[1] + direction[1])
            if is_valid_move(cells, next_cell) and next_cell not in visited and next_cell not in queue:
                queue.append(next_cell)
                parent[next_cell] = current
        index += 1

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def start_a_star(cells, model: Model):
    index = 0
    start = (0,0)
    end = (0,0)
    for cell in cells.values():
        if cell.cellType == CellType.BEGIN:
            start = cell.location
        elif cell.cellType == CellType.END:
            end = cell.location

    open_set = []
    visited = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {cell: float('inf') for cell in cells}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in cells}
    f_score[start] = heuristic(start, end)
    current = start

    while open_set:
        if(model.on_pause.get()):
            tkpause(model.on_pause)
            
        visited.append(current)
        cells[current].create_circle(CELL_SIZE/2, CELL_SIZE/2, CELL_SIZE/3, fill="#ff6352", outline="#ff6352", tags='alg')
        cells[current].create_circle(CELL_SIZE/2+(CELL_SIZE/3)*cos(radians(45)), CELL_SIZE/2+(CELL_SIZE/3)*sin(radians(45)), CELL_SIZE/5, fill="#6352ff", outline="#6352ff", tags='alg')
        cells[current].create_text(CELL_SIZE/2+(CELL_SIZE/3)*cos(radians(45)), CELL_SIZE/2+(CELL_SIZE/3)*sin(radians(45))-1, fill="#fff", text=f"{f_score[current]}", tags='alg')

        #cells[current].create_circle(CELL_SIZE/2-(CELL_SIZE/3)*cos(radians(45)), CELL_SIZE/2+(CELL_SIZE/3)*sin(radians(45)), CELL_SIZE/5, fill="#63ff52", outline="#63ff52", tags='alg')
        #cells[current].create_text(CELL_SIZE/2-(CELL_SIZE/3)*cos(radians(45)), CELL_SIZE/2+(CELL_SIZE/3)*sin(radians(45))-1, fill="#000", text=f"{g_score[current]}", tags='alg')


        cells[current].create_text(CELL_SIZE/2, CELL_SIZE/2-1, fill="#000", text=f"{index}", tags='alg')
        _, current = heappop(open_set)

        if cells[current].cellType == CellType.END:
            break

        cells[current].create_circle(CELL_SIZE/2, CELL_SIZE/2, CELL_SIZE/3, fill="#697ef5", outline="#697ef5", tags='alg')  # Blue for visited
        tksleep(0.1*model.speed_var.get())

        for direction in [NORTH, EAST, SOUTH, WEST]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if not is_valid_move(cells, neighbor):
                continue

            tentative_g_score = g_score[current] + 1  # Assume each move costs 1
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
                if neighbor not in [i[1] for i in open_set]:
                    heappush(open_set, (f_score[neighbor], neighbor))

            if neighbor not in visited:
                cells[neighbor].create_circle(CELL_SIZE/2, CELL_SIZE/2, CELL_SIZE/3, fill="#63ff52", outline="#63ff52", tags='alg')
                cells[neighbor].create_circle(CELL_SIZE/2+(CELL_SIZE/3)*cos(radians(45)), CELL_SIZE/2+(CELL_SIZE/3)*sin(radians(45)), CELL_SIZE/5, fill="#6352ff", outline="#6352ff", tags='alg')
                cells[neighbor].create_text(CELL_SIZE/2+(CELL_SIZE/3)*cos(radians(45)), CELL_SIZE/2+(CELL_SIZE/3)*sin(radians(45))-1, fill="#fff", text=f"{f_score[neighbor]}", tags='alg')

        index += 1