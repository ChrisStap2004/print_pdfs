import time
import subprocess
import os
from tkinter import messagebox



from input_information import InputInformation



class PDFProcessor():
    def __init__(self, printer_manager):
        self.printer_manager = printer_manager
        self.filepaths_to_be_printed = []

        # initialize scripts
        self.acrobat_path = r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe" 
        self.ghostscript_path = r"C:\Program Files\gs\gs10.04.0\bin\gswin64c.exe"
        self.printer = self.printer_manager.get_selected_printer()


    def get_filepaths_to_be_printed(self):
        return self.filepaths_to_be_printed
    

    def set_filepaths_to_be_printed(self, filepaths_to_be_printed):
        self.filepaths_to_be_printed = filepaths_to_be_printed


    # extract files from folder and put it into 'files list
    def plan_to_print_files(self, files_list, progress_bar, label_files, status_text):
        self.progress_bar = progress_bar
        self.label_files = label_files

        for filepath in files_list:
    
            if os.path.exists(filepath) and filepath.lower().endswith(".pdf"):
                self.filepaths_to_be_printed.append({"filepath": filepath, "copies": 1, "print": False})

            elif not filepath.lower().endswith(".pdf"):
                messagebox.ERROR(InputInformation.get_error_msg('no_pdf_file_in_files'))
                status_text.set(InputInformation.get_status_text('process_canceled'))
                print('Mindestens eine Datei ist keine pdf. Bitte wiederholen Sie die Eingabe.')
                self.filepaths_to_be_printed = []
                self.progress_bar['Value'] = 0
                self.label_folder.config(text=InputInformation.get_folder_drop_init())
                self.label_folder.update_idletasks()
                return
            
            elif not os.path.exists(filepath):
                messagebox.ERROR(InputInformation.get_error_msg('none_existing_path'))
                status_text.set(InputInformation.get_status_text('process_canceled'))
                print('Mindestens ein Pfad zu einer Datei existiert nicht. Bitte wiederholen Sie die Eingabe.')
                self.filepaths_to_be_printed = []
                self.progress_bar['Value'] = 0
                self.label_folder.config(text=InputInformation.get_folder_drop_init())
                self.label_folder.update_idletasks()
                return

        status_text.set(InputInformation.get_status_text('read_files_successful'))
        print(f'Dateien der Dateienliste eingelesen')    


    def plan_to_print_folder(self, folder_path, progress_bar, label_folder, status_text):
        self.progress_bar = progress_bar
        self.label_files = label_folder
        
        for file in os.listdir(folder_path):
            filepath = os.path.join(folder_path, file)
            if os.path.isfile(filepath) and filepath.lower().endswith(".pdf") and os.path.exists(filepath):
                filepath = os.path.join(folder_path, file)
                self.filepaths_to_be_printed.append({"filepath": filepath, "copies": 1, "print": False})

            elif not os.path.isfile(os.path.join(folder_path, file)):
                messagebox.ERROR(InputInformation.get_error_msg('folder_consist_of_not_only_files'))
                status_text.set(InputInformation.get_status_text('process_canceled'))
                print('Die Eingegebenen Dateien sind nicht vom Typ Dateien. Bitte Wiederholen Sie die Eingabe.')
                # reset inputs
                self.filepaths_to_be_printed = []
                self.progress_bar['Value'] = 0
                self.label_folder.config(text=InputInformation.get_folder_drop_init())
                self.label_folder.update_idletasks()
                return

            elif not filepath.lower().endswith(".pdf"):
                messagebox.ERROR(InputInformation.get_error_msg('no_pdf_file_in_files'))
                status_text.set(InputInformation.get_status_text('process_canceled'))
                print('Mindestens eine Datei ist keine pdf. Bitte wiederholen Sie die Eingabe.')
                self.filepaths_to_be_printed = []
                self.progress_bar['Value'] = 0
                self.label_folder.config(text=InputInformation.get_folder_drop_init())
                self.label_folder.update_idletasks()
                return
            
            elif not os.path.exists(filepath):
                messagebox.ERROR(InputInformation.get_error_msg('none_existing_path'))
                status_text.set(InputInformation.get_status_text('process_canceled'))
                print('Mindestens ein Pfad zu einer Datei existiert nicht. Bitte wiederholen Sie die Eingabe.')
                self.filepaths_to_be_printed = []
                self.progress_bar['Value'] = 0
                self.label_folder.config(text=InputInformation.get_folder_drop_init())
                self.label_folder.update_idletasks()
                return

        status_text.set(InputInformation.get_status_text('read_files_successful'))
        print(f'Dateien des Ordners eingelesen')


    def print_input(self, status_text):
        
        if len(self.filepaths_to_be_printed) > 0:
            cnt_files = len(self.filepaths_to_be_printed)
            for idx, file in enumerate(self.filepaths_to_be_printed, 1):
                print(f"Drucke {file['filepath']} auf {self.printer}...")
                # Subprozess zum Drucken der PDF-Datei mit Ghostscript
                subprocess.run([self.ghostscript_path, 
                                "-dBATCH",     # Batch-Modus, keine Benutzerinteraktion
                                "-dNOPAUSE",   # Keine Pause zwischen den Seiten
                                "-dQUIET",     # Keine Ausgaben in der Konsole
                                "-sDEVICE=mswinpr2",  # Windows Drucker
                                f"-sOutputFile=%printer%{self.printer}",  # Druckername
                                file["filepath"]], shell=True)
                
                # Fortschrittsbalken aktualisieren
                self.progress_bar['value'] = (idx / cnt_files) * 100
                self.label_files.config(text=f"{idx}/{cnt_files} Dateien verarbeitet...")
                self.label_files.update_idletasks()  # UI aktualisieren

                time.sleep(0.01)

            status_text.set(InputInformation.get_status_text('all_files_printed'))
            self.label_files.config(text=f"Alle {cnt_files} Dateien wurden gedruckt!")

        else:
            status_text.set(InputInformation.get_status_text('init'))
            messagebox.INFO("Es sing keine Dateien ausgewählt.")
            print('Es sing keine Dateien ausgewählt.')