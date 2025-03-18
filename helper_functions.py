import os
import tkinter as tk
from tkinter import messagebox
from input_information import InputInformation

class helper_functions():
    def __init__(self):
        pass

    def validate_int_input(P):
        if P == "" or P.isdigit():
            return True
        return False
    
    def open_readme(self, root):
        help_window = tk.Toplevel(root)
        help_window.title("Hilfe")
        help_window.geometry(InputInformation.get_root_geometrie())
        help_window.geometry(f"+{root.winfo_x()}+{root.winfo_y()}")

        with open('readme.txt', 'r') as file:
            help_text = file.read()

        help_label = tk.Label(help_window, text=help_text, padx=10, pady=10, wraplength=380, justify="left")
        help_label.pack(expand=True, fill='both')

        #try:
        #    os.startfile(os.path.join(os.getcwd(), 'readme.txt'))
        #except Exception as e:
        #    messagebox.showerror("Fehler", f"Die Datei konnte nicht geöffnet werden: {e}")
