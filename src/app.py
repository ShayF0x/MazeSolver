import tkinter as tk
from model.model import Model
from view.view import View
from controller.controller import Controller

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('MazeSolver')
        width= self.winfo_screenwidth()
        height= self.winfo_screenheight()
        self.state('zoom')
        self.attributes('-fullscreen', True)

        self.geometry("%dx%d" % (width, height))

        # create a model
        model = Model()

        # create a view and place it on the root window
        view = View(self)
        view.pack(fill="both", expand=True, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()
    