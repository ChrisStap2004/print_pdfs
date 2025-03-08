import os
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD, DND_FILES

from input_information import InputInformation

class PDFPrinterApp:
    def __init__(self, printer_manager, pdf_processor):
        self.printer_manager = printer_manager
        self.pdf_processor = pdf_processor

        # initialize main-window
        self.root = TkinterDnD.Tk()
        self.root.title(InputInformation.get_root_title)
        self.root.geometry(InputInformation.get_root_geometrie)
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


    # create the print-overwiev window
    def creater_print_overview(self):
        self.overview_window = tk.Toplevel(self.root)
        self.overview_window.title("Dateiübersicht")

        if not self.pdf_processor.get_filepaths_to_be_printed():
            print(f'Keine Dateien zum Drucken hinzugefügt.')
            return
        
        # display every filename and let user choose how many copies he wants
        for idx, file in enumerate(self.pdf_processor.get_filepaths_to_be_printed()):
            frame = tk.Frame(self.overview_window)
            frame.pack(pady=5, padx=5)
            # filename
            filename_label = tk.Label(frame, text=os.path.basename(file["filename"]))
            filename_label.pack(side=tk.Left)
            # cnt of copies
            copies_label = tk.Label(frame, text="Kopien:")
            copies_label.pack(side=tk.LEFT)
            copies_entry = tk.Entry(frame)
            copies_entry.insert(0, file["copies"])
            copies_entry.pack(side=tk.LEFT)
            # checkbox for oppurtunity of printing
            print_var = tk.BooleanVar(True)
            print_checkbox = tk.Checkbutton(frame, text="Drucken", variable=print_var)
            print_checkbox.pack(side=tk.LEFT)
            # safe references
            file["copies_entry"] = copies_entry
            file["print_val"] = print_var

        print_button = tk.Button(self.overview_window, text='Drucken', command=self.pdf_processor.print_input)
        print_button.pack(pady=10)

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
        self.label_folder.config(text=InputInformation.get_printing())
        # Dateien drucken
        self.pdf_processor.plan_to_print_folder(ordnerpfad, self.progress_bar, self.label_folder)


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
            self.label_files.config(text=InputInformation.get_printing())
            self.pdf_processor.plan_to_print_files(files_list, self.progress_bar, self.label_files)


    def create_widgets(self):
        # create sub-windows: file, folder, bar
        self.folder_frame = tk.Frame(self.root, width=400, height=300, bd=2, relief='groove')
        self.folder_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.files_frame = tk.Frame(self.root, width=400, height=300, bd=2, relief='groove')
        self.files_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        self.bar_frame = tk.Frame(self.root, width=400, height=100, bd=2, relief='groove')
        self.bar_frame.grid(row=1, columnspan=2, padx=5, pady=5, sticky='nsew')
        self.bar_frame.grid_columnconfigure(0, weight=20)
        self.bar_frame.grid_columnconfigure(0, weight=1)

        # labels for windows
        self.label_folder = tk.Label(self.folder_frame, text=InputInformation.get_folder_drop_init(), padx=10, pady=10)
        self.label_folder.pack(fill='both', expand=True, padx=20, pady=20)

        self.label_files = tk.Label(self.files_frame, text=InputInformation.get_files_drop_init(), padx=10, pady=10)
        self.label_files.pack(fill='both', expand=True, padx=20, pady=20)

        # create process-bar
        self.progress_bar = ttk.Progressbar(self.bar_frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(side='left', expand=True, pady=20, padx=10)
        # create print-button
        self.print_button = ttk.Button(self.bar_frame, text='Drucken',command=self.pdf_processor.print_input)
        self.print_button.pack(side='right', pady=10, padx=10)

        # Drag & Drop auf das Fenster ermöglichen
        self.folder_frame.drop_target_register(DND_FILES)
        self.folder_frame.dnd_bind('<<Drop>>', self.on_folder_drop)

        self.files_frame.drop_target_register(DND_FILES)
        self.files_frame.dnd_bind('<<Drop>>', self.on_files_drop)


    def run(self):
        self.root.mainloop()