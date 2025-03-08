import os
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD, DND_FILES

class PDFPrinterApp:
    def __init__(self, printer_manager):
        self.printer_manager = printer_manager

        # initialize main-window
        self.root = TkinterDnD.Tk()
        self.root.title("Drucken von PDF in Eingabeform von Dateien oder Ordner")
        self.root.geometry("800x400")
        self.root.grid_rowconfigure(0, weight=5)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # create menubar
        self.create_menubar()
        # create widgets
        self.create_widgets()


    # create menubar
    def create_menubar(self):
        # create a menubar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # create file-menu
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label='Wähle Dateien')
        file_menu.add_command(label='Wähle Ordner')
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.root.destroy)

        # create settings-menu
        settings_menu = tk.Menu(menubar, tearoff=False)
        # create submenu
        printer_menu = tk.Menu(settings_menu, tearoff=0)
        for printer in self.printer_manager.printers:
            printer_menu.add_command(label=printer, command= lambda p=printer: self.printer_manager.set_printer(p))
        # adding submenu
        settings_menu.add_cascade(label='Drucker Auswählen:', menu=printer_menu)

        # adding submenus to menubar
        menubar.add_cascade(label='File', menu=file_menu, underline=0)
        menubar.add_cascade(label='Settings', menu=settings_menu, underline=0)



    # drag and drop of folder
    def on_folder_drop(self, event):
        ordnerpfad = event.data.strip('{}')  # Der Ordnerpfad, der vom Benutzer gezogen wurde
        # check data_format
        if not os.path.isdir(ordnerpfad):
            print("Sie haben keinen Ordner abgelegt. Bitte wiederholen")
            return
        
        print(f"Ordner ausgewählt: {ordnerpfad}")
        # Fortschrittsbalken auf 0 setzen
        self.progress_bar['value'] = 0
        self.label_folder.config(text="Druckvorgang läuft...")
        # Dateien drucken
        self.pdf_processor.print_folder(ordnerpfad)


    # drag and drop of files
    def on_files_drop(self, event):
            files_list = event.data.split('} {')  # Der Pfad der Datei, die auf das rechte Drop-Ziel gezogen wurde
            
            for i in range(len(files_list)):
                files_list[i] = files_list[i].strip('{').strip('}')
                
                if not (os.path.isfile(files_list[i]) and files_list[i].lower().endswith(".pdf")):
                    print("Erwarteter Datentyp .pdf nicht bei allen Dateien vorhanden. Wiederholen Sie den Vorgang")
                    return
                
            print(f"Dateien ausgewählt: {files_list}")
            # Fortschrittsbalken auf 0 setzen und die Datei drucken
            self.progress_bar['value'] = 0
            self.label_files.config(text="Druckvorgang läuft...")
            self.pdf_processor.print_files(files_list)


    def create_widgets(self):
        # create sub-windows: file, folder, bar
        self.folder_frame = tk.Frame(self.root, width=400, height=300, bd=2, relief='groove')
        self.folder_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.files_frame = tk.Frame(self.root, width=400, height=300, bd=2, relief='groove')
        self.files_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        self.bar_frame = tk.Frame(self.root, width=400, height=100, bd=2, relief='groove')
        self.bar_frame.grid(row=1, columnspan=2, padx=5, pady=5, sticky='nsew')

        # labels for windows
        self.label_folder = tk.Label(self.folder_frame, text="Ziehen Sie einen Ordner hierher, um die PDFs zu drucken.", padx=10, pady=10)
        self.label_folder.pack(fill='both', expand=True, padx=20, pady=20)

        self.label_files = tk.Label(self.files_frame, text="Ziehen Sie versch. Dateien hierher, um die PDFs zu drucken.", padx=10, pady=10)
        self.label_files.pack(fill='both', expand=True, padx=20, pady=20)

        # create process-bar
        self.progress_bar = ttk.Progressbar(self.bar_frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=20)

        # Drag & Drop auf das Fenster ermöglichen
        self.folder_frame.drop_target_register(DND_FILES)
        self.folder_frame.dnd_bind('<<Drop>>', self.on_folder_drop)

        self.files_frame.drop_target_register(DND_FILES)
        self.files_frame.dnd_bind('<<Drop>>', self.on_files_drop)


    def run(self):
        self.root.mainloop()