import os
from tkinter import messagebox

class helper_functions():
    def __init__(self):
        pass

    def validate_int_input(P):
        if P == "" or P.isdigit():
            return True
        return False
    
    def open_readme():
        try:
            os.startfile(os.path.join(os.getcwd(), 'readme.txt'))
        except Exception as e:
            messagebox.showerror("Fehler", f"Die Datei konnte nicht geöffnet werden: {e}")
