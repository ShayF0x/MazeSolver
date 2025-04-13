import os
import tkinter as tk
from tkinter import PhotoImage, ttk
from widget.cell import Cell, CellType
from PIL import Image, ImageTk

CELL_RADIUS = 17

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create Frames
        self.panel_bottom = tk.Frame(self)
        self.panel_bottom.pack(fill="x", side="bottom", pady=(10, 0))

        self.panel_right = tk.Frame(self)
        self.panel_right.pack(fill="y", side="right", padx=(10, 0))

        self.panel_left = tk.Frame(self)
        self.panel_left.pack(fill="y", side="left", padx=(0, 10))

        self.panel_center = tk.Frame(self, highlightbackground="black", highlightthickness=1)

        # create Menu
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)

        fileMenu = tk.Menu(self.menubar, tearoff=False)

        self.submenu = tk.Menu(fileMenu, tearoff=False)
        fileMenu.add_cascade(label='Theme', menu=self.submenu)

        fileMenu.add_command(label="Exit", underline=0, command=quit)
        self.menubar.add_cascade(label="Settings", menu=fileMenu)

        button_style = ttk.Style()
        button_style.configure("TButton", padding=(0, 10), background="white")  # (horizontal padding, vertical padding)

        # create Widgets
            #Panel Right
        self.button_graph = ttk.Button(self.panel_right, text="Graph")
        self.button_graph.pack(fill="x", pady=4)

        self.button_reset = ttk.Button(self.panel_right, text="Reset")
        self.button_reset.pack(fill="x", pady=4)

        self.panel_time = tk.Frame(self.panel_right)
        self.panel_time.pack(side="bottom")

        self.speed_slider = tk.Scale(self.panel_time, from_=0, to=10,orient="horizontal", tickinterval=0)
        self.speed_slider.pack(side="right")

        self.button_pause_frame = tk.Frame(self.panel_time, width=32, height=32)
        self.button_pause_frame.pack_propagate(False)  # No resize
        self.button_pause_frame.pack(side="left", anchor="s", padx=8)

        original_image = Image.open(os.getcwd()+r"\\assets\\images\\button_pause.png")
        resized_image = original_image.resize((32, 32), Image.Resampling.LANCZOS)
        toggle_icon = ImageTk.PhotoImage(resized_image)

        self.button_pause = tk.Button(self.button_pause_frame, image=toggle_icon)
        self.button_pause.image = toggle_icon
        self.button_pause.pack(fill=tk.BOTH, expand=True)

        self.label_slider = ttk.Label(self.panel_right, text="Delay")
        self.label_slider.pack(side="bottom")


            #Panel Left
        self.button_alg_1 = ttk.Button(self.panel_left, text="Depth-First Search (DFS)")
        self.button_alg_1.pack(fill="x", pady=4)

        self.button_alg_2 = ttk.Button(self.panel_left, text="Breadth-First Search (BFS)")
        self.button_alg_2.pack(fill="x", pady=4)

        self.button_alg_3 = ttk.Button(self.panel_left, text="A-Star")
        self.button_alg_3.pack(fill="x", pady=4)

        self.button_clear = ttk.Button(self.panel_left, text="Clear Cells")
        self.button_clear.pack(fill="x", pady=4)

        self.button_generate_maze = ttk.Button(self.panel_left, text="Generate maze")
        self.button_generate_maze.pack(fill="x", pady=4)

        self.label_bottom = ttk.Label(self.panel_bottom, text="Maze 1")
        self.label_bottom.pack()

        self.cells: dict[tuple[2], Cell] = {}
        for i in range(CELL_RADIUS):
            for j in range(CELL_RADIUS):
                self.panel_center.grid_rowconfigure(j, weight = 1)
                self.panel_center.grid_columnconfigure(i, weight = 1)
                cell = Cell(self.panel_center, (i, j), CellType.CLASSIC)
                cell.grid(row=j, column=i)
                self.cells[(i, j)] = cell

        self.cells[(0,1)].set_cell_type(CellType.BEGIN)
        self.cells[(16,15)].set_cell_type(CellType.END)

        # set the controller
        self.controller = None
        self.panel_center.pack(pady=1, padx=1)
        self.panel_center.pack_propagate(0)

    def set_controller(self, controller):
        """
        Set the controller\n
        Parameters:
            controller (Controller):The controller of application
        Returns:
            None
        """
        self.controller = controller

        controller.model.speed_var.set(10)
        self.speed_slider.config(variable=controller.model.speed_var)