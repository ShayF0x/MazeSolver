import re
import tkinter as tk
from widget.cell import Cell
from widget.cell import CellType
from widget.cell import CellState
from view.view import CELL_RADIUS
from enum import Enum

class Model:
    def __init__(self):
        self.maze = []
        self.speed_var = tk.IntVar()

        self.on_pause = tk.BooleanVar()
        self.on_pause.set(False)

        self.onAction = tk.BooleanVar()
        self.onAction.set(False)

    def update_maze(self, cells: list[Cell]):
        self.maze = [ [0 for i in range(CELL_RADIUS)] for i in range(CELL_RADIUS)]
        for cell in cells.values():
            if cell.cellType == CellType.BEGIN:
                self.maze[cell.location[1]][cell.location[0]] = 2
            elif cell.cellType == CellType.END:
                self.maze[cell.location[1]][cell.location[0]] = 3
            elif cell.state == CellState.EMPTY:
                self.maze[cell.location[1]][cell.location[0]] = 1

    def get_cell_orientation(self, location):
        #              nord , east , south , west
        orientation = [False, False, False, False]
        target =      [None , None , None , None ]
        x = location[0]
        y = location[1]

        if self.maze[y][x] == 0:
            return orientation, target
        
        if y != 0 and self.maze[y-1][x] != 0:
            orientation[0] = True
            target = (x, y-1)
        if x != CELL_RADIUS-1 and self.maze[y][x+1] != 0:
            orientation[1] = True
            target = (x+1, y)
        if y != CELL_RADIUS-1 and self.maze[y+1][x] != 0:
            orientation[2] = True
            target = (x, y+1)
        if x != 0 and self.maze[y][x-1] != 0:
            orientation[3] = True
            target = (x-1, y)

        return orientation, target