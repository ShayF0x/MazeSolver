
import tkinter as tk

def tksleep(t):
        'emulating time.sleep(seconds)'
        ms = int(t*1000)
        root = tk._get_default_root()
        var = tk.IntVar(root)
        root.after(ms, lambda: var.set(1))
        root.wait_variable(var)

def tkpause(var):
        'Wait until a BooleanVar becomes False'
        root = tk._get_default_root()
    
        def check_var():
                if not var.get():
                        return
                root.after(100, check_var)  # check each 100ms

        check_var()
        root.wait_variable(var)