import tkinter as tk
from enum import Enum
from PIL import Image, ImageTk
import os

#CELL_SIZE = 55
CELL_SIZE = 40

class ViewMode(Enum):
    CLASSIC = 0
    MUSEUM = 1

class CellState(Enum):
    EMPTY = 0
    FILLED = 1
    GRAPHED_EMPTY = 2
    GRAPHED_FILLED = 3

class CellType(Enum):
    BEGIN = {"color_fill":"#49eb34", "color_empty":"#49eb34", "color_fill_museum":os.getcwd()+r"\\assets\\images\\color_begin_museum.png", "color_empty_museum":os.getcwd()+r"\\assets\\images\\color_begin_museum.png"}
    CLASSIC = {"color_fill":"black", "color_empty":"white", "color_fill_museum":os.getcwd()+r"\\assets\\images\\color_fill_museum.png", "color_empty_museum":os.getcwd()+r"\\assets\\images\\color_empty_museum.png"}
    END = {"color_fill":"#eb3434", "color_empty":"#eb3434", "color_fill_museum":os.getcwd()+r"\\assets\\images\\color_end_museum.png", "color_empty_museum":os.getcwd()+r"\\assets\\images\\color_end_museum.png"}


class Cell(tk.Canvas):
    def __init__(self, parent, location: tuple[2], cellType: CellType):
        super().__init__(parent, highlightthickness=0, bg=cellType.value["color_fill"], width=CELL_SIZE, height=CELL_SIZE)
        self.mode = ViewMode.CLASSIC
        self.image = {}

        #Border
        self.create_line(0, 0, CELL_SIZE-1, 0, fill="white")
        self.create_line(0, CELL_SIZE-1, CELL_SIZE-1, CELL_SIZE-1, fill="white")
        self.create_line(CELL_SIZE-1, 0, CELL_SIZE-1, CELL_SIZE-1, fill="white")
        self.create_line(0, 0, 0, CELL_SIZE-1, fill="white")

        self.cellType=cellType
        self.state = CellState.FILLED
        # (x, y)
        self.location = location 
    
    def update(self, mode=None, root=None):
        if mode != None:
            self.mode = mode
        self.delete('graphs')
        self.delete('alg')
        self.delete('image')
        match self.state:
            case CellState.EMPTY | CellState.GRAPHED_EMPTY:
                if self.mode == ViewMode.CLASSIC:
                    self.configure(background=self.cellType.value["color_empty"])
                elif self.mode == ViewMode.MUSEUM:
                    self.configure(background=self.cellType.value["color_empty"])
                    my_img = (Image.open(self.cellType.value["color_empty_museum"]))
                    resized_img = my_img.resize((CELL_SIZE,CELL_SIZE), Image.LANCZOS)
                    self.image[self.location] = ImageTk.PhotoImage(resized_img)
                    self.create_image((0, 0), image = self.image[self.location], anchor='nw', tags='image')
                return
            case CellState.FILLED | CellState.GRAPHED_FILLED:
                if self.mode == ViewMode.CLASSIC:
                    self.configure(background=self.cellType.value["color_fill"])
                elif self.mode == ViewMode.MUSEUM:
                    self.configure(background=self.cellType.value["color_fill"])
                    my_img = (Image.open(self.cellType.value["color_fill_museum"]))
                    resized_img = my_img.resize((CELL_SIZE,CELL_SIZE), Image.LANCZOS)
                    self.image[self.location] = ImageTk.PhotoImage(resized_img)
                    self.create_image((0, 0), image = self.image[self.location], anchor='nw', tags='image')
                return
            case _:
                return

    def set_cell_type(self, cellType):
        self.cellType = cellType
        self.update()

    def set_cell_state(self, state):
        self.state = state
        self.update()

    def is_clicked(self):
        if not self.state is CellState.GRAPHED_FILLED and not self.state is CellState.GRAPHED_EMPTY:
            self.set_cell_state([CellState.EMPTY, CellState.FILLED][([CellState.EMPTY, CellState.FILLED].index(self.state)+1)%2])

    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def create_circle_arc(self, x, y, r, **kwargs):
        if "start" in kwargs and "end" in kwargs:
            kwargs["extent"] = kwargs.pop("end") - kwargs["start"]
        return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)

    

