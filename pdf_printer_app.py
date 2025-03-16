import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES

from input_information import InputInformation

class PDFPrinterApp:
    def __init__(self, printer_manager, pdf_processor):
        self.printer_manager = printer_manager
        self.pdf_processor = pdf_processor

        # initialize main-window
        self.root = TkinterDnD.Tk()
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_close('root'))
        self.root.title(InputInformation.get_root_title())
        self.root.geometry(InputInformation.get_root_geometrie())
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
        file_menu.add_command(label='Wähle Dateien', command=self.open_files)
        file_menu.add_command(label='Wähle Ordner', command=self.open_folder)
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
        # creating printing queue
        settings_menu.add_cascade(label="Druckerwarteschlange", command=self.printer_manager.open_printing_queue)

        # adding submenus to menubar
        menubar.add_cascade(label='File', menu=file_menu, underline=0)
        menubar.add_cascade(label='Settings', menu=settings_menu, underline=0)

    def open_folder(self):
        self.folder_selected = filedialog.askdirectory(title='Wählen Sie einen zu druckenden Ordner aus indem die PDF-Dateien enthalten sind')
        if self.folder_selected:
            print(f"Chosen folder: {self.folder_selected}")
            self.progress_bar['value'] = 0
            self.label_folder_text.set(InputInformation.get_printing())
            self.pdf_processor.plan_to_print_folder(self.folder_selected, self.progress_bar, self.label_folder)

            if len(self.pdf_processor.get_filepaths_to_be_printed()) > 0:
                    self.create_print_overview()

    def open_files(self):
        self.files_selected =filedialog.askopenfilenames(
            filetypes=[("PDF Dateien", "*.pdf")], 
            title='Wählen Sie die zu druckenden PDF-Dateien aus')
        if self.files_selected:
            self.files_selected = list(self.files_selected)
            print(f"Chosen files: {self.files_selected}")
            
            self.progress_bar['value'] = 0
            self.label_files_text.set(InputInformation.get_printing())
            self.pdf_processor.plan_to_print_files(self.files_selected, self.progress_bar, self.label_files)

            if len(self.pdf_processor.get_filepaths_to_be_printed()) > 0:
                self.create_print_overview()

    def on_close(self, key):
        if key == 'overview_window':
            self.pdf_processor.set_filepaths_to_be_printed([])
            self.overview_window.destroy()
            self.label_folder_text.set(InputInformation.get_folder_drop_init())
            self.label_files_text.set(InputInformation.get_files_drop_init())
            self.root.focus
        elif key == 'root':
            self.printer_manager.close_printing_queue()
            self.root.destroy()


    def on_print_button_click(self):
        self.overview_window.destroy()
        self.pdf_processor.print_input()

    # create the print-overwiev window
    def create_print_overview(self):
        self.overview_window = tk.Toplevel(self.root)
        self.overview_window.title("Dateiübersicht")
        self.overview_window.geometry(InputInformation.get_overview_geometrie())
        self.overview_window.grab_set()
        self.overview_window.focus_set()
        self.overview_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close('overview_window'))
        # set window same position as root
        self.overview_window.geometry(f"+{self.root.winfo_x()}+{self.root.winfo_y()}")

        if not self.pdf_processor.get_filepaths_to_be_printed():
            print(f'Keine Dateien zum Drucken hinzugefügt.')
            return
        else:
            # name first row
            table_frame = ttk.Frame(self.overview_window)
            table_frame.grid(row=0, columnspan=3, padx=5, pady=5)
            ttk.Label(table_frame, text="Dateiname").grid(row=0, column=0, padx=5, pady=5)
            ttk.Label(table_frame, text="Kopien").grid(row=0, column=1, padx=5, pady=5)
            ttk.Label(table_frame, text="Drucken").grid(row=0, column=2, padx=5, pady=5)
            # display every filename and let user choose how many copies he wants
            for idx, file in enumerate(self.pdf_processor.get_filepaths_to_be_printed(), 1):
                # filename
                filename_label = ttk.Label(table_frame, text=os.path.basename(file["filepath"]))
                filename_label.grid(row=idx, column=0, padx=5, pady=5)
                # cnt of copies
                copies_entry = ttk.Entry(table_frame)
                copies_entry.insert(0, file["copies"])
                copies_entry.grid(row=idx, column=1, padx=5, pady=5)
                # checkbox for oppurtunity of printing
                print_var = tk.BooleanVar()
                print_var.set(True)
                print_checkbox = ttk.Checkbutton(table_frame, text="Drucken", variable=print_var)
                print_checkbox.grid(row=idx, column=2, padx=5,)
                # safe references
                file["copies_entry"] = copies_entry
                file["print_val"] = print_var

            print_frame = ttk.Frame(self.overview_window)
            print_frame.grid(row=1, column=3, padx=5, pady=5)
            print_button = ttk.Button(print_frame, text='Drucken', command=self.on_print_button_click)
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
        self.label_folder_text.set(InputInformation.get_printing())
        self.pdf_processor.plan_to_print_folder(ordnerpfad, self.progress_bar, self.label_folder)

        if len(self.pdf_processor.get_filepaths_to_be_printed()) > 0:
                self.create_print_overview()

    # drag and drop of files
    def on_files_drop(self, event):
            files_list = event.data.split('} {')  # Der Pfad der Datei, die auf das rechte Drop-Ziel gezogen wurde
            
            for i in range(len(files_list)):
                files_list[i] = files_list[i].strip('{').strip('}')
                
                if not (os.path.isfile(files_list[i]) and files_list[i].lower().endswith(".pdf")):
                    print("Erwarteter Datentyp .pdf nicht bei allen Dateien vorhanden. Wiederholen Sie den Vorgang")
                    return
                
            print(f"Chosen files: {files_list}")
            # Fortschrittsbalken auf 0 setzen und die Datei drucken
            self.progress_bar['value'] = 0
            self.label_files_text.set(InputInformation.get_printing())
            self.pdf_processor.plan_to_print_files(files_list, self.progress_bar, self.label_files)
            
            if len(self.pdf_processor.get_filepaths_to_be_printed()) > 0:
                self.create_print_overview()



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
        self.label_folder_text = tk.StringVar(value=InputInformation.get_folder_drop_init())
        self.label_folder = tk.Label(self.folder_frame, textvariable=self.label_folder_text, padx=10, pady=10)
        self.label_folder.pack(fill='both', expand=True, padx=20, pady=20)

        self.label_files_text = tk.StringVar(value=InputInformation.get_files_drop_init())
        self.label_files = tk.Label(self.files_frame, textvariable=self.label_files_text, padx=10, pady=10)
        self.label_files.pack(fill='both', expand=True, padx=20, pady=20)

        # create process-bar
        self.progress_bar = ttk.Progressbar(self.bar_frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(side='left', expand=True, pady=20, padx=10)
        # create print-button
        #self.print_button = ttk.Button(self.bar_frame, text='Drucken',command=self.pdf_processor.print_input)
        #self.print_button.pack(side='right', pady=10, padx=10)

        # Drag & Drop auf das Fenster ermöglichen
        self.folder_frame.drop_target_register(DND_FILES)
        self.folder_frame.dnd_bind('<<Drop>>', self.on_folder_drop)

        self.files_frame.drop_target_register(DND_FILES)
        self.files_frame.dnd_bind('<<Drop>>', self.on_files_drop)


    def run(self):
        self.root.mainloop()