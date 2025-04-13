import os
from view.view import View
from widget.cell import CellState
from widget.cell import CELL_SIZE
from widget.cell import CellState
from utils.maze_generator import *
from utils.tkinter_process import *
from model.model import Model
from widget.cell import ViewMode
from utils.algorythme_solve import *
from PIL import Image, ImageTk


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.cell_focus_mode = None

        view.panel_center.bindtags(("special",) + view.panel_center.bindtags())
        for cell in view.cells.values():
            cell.bindtags(("special",) + cell.bindtags())
        view.panel_center.bind_class("special", "<B1-Motion>", self.event_mouse_move_center)
        view.panel_center.bind_class("special", "<Button-1>", self.event_mouse_move_center)
        view.panel_center.bind_class("special", "<ButtonRelease-1>", self.event_button_release_center)

        view.button_generate_maze.configure(command=self.button_click_generate_maze)
        view.button_graph.configure(command=self.button_click_generate_graph)
        view.button_reset.configure(command=self.button_click_reset)

        view.button_alg_1.configure(command=self.algorithme_profondeur)
        view.button_alg_2.configure(command=self.algorithme_largeur)
        view.button_alg_3.configure(command=self.algorithme_astar)
        view.button_clear.configure(command=self.clear_algorithme)

        view.button_pause.configure(command=self.button_click_pause)

        view.submenu.add_command(label="Default", command=self.menu_file_mode_classic_clicked)
        view.submenu.add_command(label="Museum", command=self.menu_file_mode_museum_clicked)

        model.onAction.trace_add("write", self.event_on_action_changed)

    def event_mouse_move_center(self, event):
        for cell in self.view.cells.values():
            if self.is_in_area_square(cell.winfo_rootx(), cell.winfo_rooty(), CELL_SIZE, CELL_SIZE, event.x_root, event.y_root):
                if cell.state != CellState.GRAPHED_FILLED and cell.state != CellState.GRAPHED_EMPTY:
                    if self.cell_focus_mode == None:
                        self.cell_focus_mode = [CellState.EMPTY, CellState.FILLED][([CellState.EMPTY, CellState.FILLED].index(cell.state) + 1) % 2]
                        cell.set_cell_state(self.cell_focus_mode)
                    else:
                        cell.set_cell_state(self.cell_focus_mode)

    def event_on_action_changed(self, *args):
        self.view.button_alg_1.configure(state=["normal", "disabled"][self.model.onAction.get()])
        self.view.button_alg_2.configure(state=["normal", "disabled"][self.model.onAction.get()])
        self.view.button_alg_3.configure(state=["normal", "disabled"][self.model.onAction.get()])
        self.view.button_clear.configure(state=["normal", "disabled"][self.model.onAction.get()])
        self.view.button_generate_maze.configure(state=["normal", "disabled"][self.model.onAction.get()])
        self.view.button_graph.configure(state=["normal", "disabled"][self.model.onAction.get()])
        self.view.button_reset.configure(state=["normal", "disabled"][self.model.onAction.get()])
        

    def event_button_release_center(self, event):
        self.cell_focus_mode = None
    
    def button_click_pause(self):
        self.model.on_pause.set(not self.model.on_pause.get())

        original_image = Image.open([os.getcwd()+r"\\assets\\images\\button_pause.png", os.getcwd()+r"\\assets\\images\\button_play.png"][self.model.on_pause.get()])
        resized_image = original_image.resize((32, 32), Image.Resampling.LANCZOS)
        toggle_icon = ImageTk.PhotoImage(resized_image)

        self.view.button_pause.configure(image=toggle_icon)
        self.view.button_pause.image = toggle_icon

    def algorithme_profondeur(self):
        if self.model.onAction.get():
            return
    
        self.model.onAction.set(True)

        for cell in self.view.cells.values():
            if cell.state is CellState.GRAPHED_EMPTY:
                    cell.set_cell_state(CellState.EMPTY)
            elif cell.state is CellState.GRAPHED_FILLED:
                    cell.set_cell_state(CellState.FILLED)

            cell.update()

        self.clear_algorithme()        
        self.model.update_maze(self.view.cells)
        start_dfs(self.view.cells, self.model)

        self.model.onAction.set(False)

    def algorithme_largeur(self):
        if self.model.onAction.get():
            return
    
        self.model.onAction.set(True)

        for cell in self.view.cells.values():
            if cell.state is CellState.GRAPHED_EMPTY:
                    cell.set_cell_state(CellState.EMPTY)
            elif cell.state is CellState.GRAPHED_FILLED:
                    cell.set_cell_state(CellState.FILLED)

            cell.update()

        self.clear_algorithme()        
        self.model.update_maze(self.view.cells)
        start_bfs(self.view.cells, self.model)

        self.model.onAction.set(False)

    def algorithme_astar(self):
        if self.model.onAction.get():
            return
    
        self.model.onAction.set(True)

        for cell in self.view.cells.values():
            if cell.state is CellState.GRAPHED_EMPTY:
                    cell.set_cell_state(CellState.EMPTY)
            elif cell.state is CellState.GRAPHED_FILLED:
                    cell.set_cell_state(CellState.FILLED)

            cell.update()

        self.clear_algorithme()
        self.model.update_maze(self.view.cells)
        start_a_star(self.view.cells, self.model)

        self.model.onAction.set(False)

    def clear_algorithme(self):
        if self.model.onAction.get():
            return
    
        self.model.onAction.set(True)

        for cell in self.view.cells.values():
             cell.update(cell.mode)

        self.model.update_maze(self.view.cells)

        self.model.onAction.set(False)

    def button_click_reset(self):
        if self.model.onAction.get():
            return
    
        self.model.onAction.set(True)

        self.view.label_bottom.config(text="Reset  ... [0%]")
        i = 0
        for cell in self.view.cells.values():
            percent = i/len(self.view.cells)
            self.view.label_bottom.config(text=f"Reset ... [{percent}]")
            cell.set_cell_state(CellState.FILLED)
            i+=1
        self.view.label_bottom.config(text="Maze")

        self.model.onAction.set(False)

    def button_click_generate_maze(self):
        if self.model.onAction.get():
            return
    
        self.model.onAction.set(True)

        for cell in self.view.cells.values():
            if cell.state is CellState.GRAPHED_EMPTY:
                    cell.set_cell_state(CellState.EMPTY)
            elif cell.state is CellState.GRAPHED_FILLED:
                    cell.set_cell_state(CellState.FILLED)

            cell.update()

        xMax, yMax = 8, 8
        for y in range(yMax*2):
            for x in range(xMax*2):
                if x % 2 != 0 and y % 2 != 0:
                    self.view.cells[(x, y)].set_cell_state(CellState.EMPTY)
                else:
                    self.view.cells[(x, y)].set_cell_state(CellState.FILLED)

        self.view.label_bottom.config(text=f"Generation of a maze  ...")

        generate_labyrinthe(xMax, yMax, self.view.cells, self.model)

        for cell in self.view.cells.values():
             cell.update(cell.mode)
             
        self.view.label_bottom.config(text="Maze")

        self.model.onAction.set(False)
        
    def button_click_generate_graph(self):
        if self.model.onAction.get():
            return
    
        self.model.onAction.set(True)

        self.model.update_maze(self.view.cells)

        for y in range(len(self.model.maze)):
            for x in range(len(self.model.maze[y])):
                cell = self.view.cells[(x,y)]

                if cell.state is CellState.EMPTY:
                    cell.set_cell_state(CellState.GRAPHED_EMPTY)
                elif cell.state is CellState.FILLED:
                    cell.set_cell_state(CellState.GRAPHED_FILLED)

                orientation, target = self.model.get_cell_orientation((x, y))

                if orientation[0] == True:
                    cell.create_line(CELL_SIZE/2, CELL_SIZE/2, CELL_SIZE/2, 0, fill="#000", tags='graphs')
                if orientation[1] == True:
                    cell.create_line(CELL_SIZE/2, CELL_SIZE/2, CELL_SIZE, CELL_SIZE/2, fill="#000", tags='graphs')
                if orientation[2] == True:
                    cell.create_line(CELL_SIZE/2, CELL_SIZE/2, CELL_SIZE/2, CELL_SIZE, fill="#000", tags='graphs')
                if orientation[3] == True:
                    cell.create_line(CELL_SIZE/2, CELL_SIZE/2, 0, CELL_SIZE/2, fill="#000", tags='graphs')

                if orientation.count(True) == 1:
                    cell.create_circle(CELL_SIZE/2, CELL_SIZE/2, CELL_SIZE/3, fill="#ff6352", outline="#ff6352", tags='graphs')
                elif orientation.count(True) == 2:
                    cell.create_circle(CELL_SIZE/2, CELL_SIZE/2, CELL_SIZE/3, fill="#fff", outline="#ff6352", tags='graphs')
                elif orientation.count(True) == 3 or orientation.count(True) == 4:
                    cell.create_rectangle(CELL_SIZE/5, CELL_SIZE/3, CELL_SIZE-CELL_SIZE/5, CELL_SIZE-CELL_SIZE/3, fill="#ff6352", outline="#ff6352", tags='graphs')  
                
                
                if self.model.maze[y][x] != 0:
                    cell.create_text(CELL_SIZE/2, CELL_SIZE/2-1, fill="#000", text=f"({x}, {y})", tags='graphs')

                tksleep(0.01*self.model.speed_var.get())

        self.model.onAction.set(False)

    def is_in_area_square(self, x, y, width, height, x_pointer, y_pointer):
        return x <= x_pointer <= x + width and y <= y_pointer <= y + height
    
    def menu_file_mode_classic_clicked(self):
        for cell in self.view.cells.values():
             cell.update(ViewMode.CLASSIC)
    
    def menu_file_mode_museum_clicked(self):
         for cell in self.view.cells.values():
             cell.update(ViewMode.MUSEUM)
