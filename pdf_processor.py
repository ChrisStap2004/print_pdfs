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
        self.ghostscript_path = InputInformation.get_ghostscript_path()
        self.printer = self.printer_manager.get_selected_printer()

        self.label_files_text = None
        self.label_folder_text = None


    def get_filepaths_to_be_printed(self):
        return self.filepaths_to_be_printed
    

    def set_filepaths_to_be_printed(self, filepaths_to_be_printed):
        self.filepaths_to_be_printed = filepaths_to_be_printed


    # extract files from folder and put it into 'files list
    def plan_to_print_files(self, files_list, progress_bar, label_files_text, status_text):
        self.progress_bar = progress_bar
        self.label_files_text = label_files_text

        for filepath in files_list:
    
            if os.path.exists(filepath) and filepath.lower().endswith(".pdf"):
                self.filepaths_to_be_printed.append({"filepath": filepath, "copies": 1, "print": False})

            elif not filepath.lower().endswith(".pdf"):
                messagebox.showerror("Fehler", InputInformation.get_error_msg('no_pdf_file_in_files'))
                status_text.set(InputInformation.get_status_text('process_canceled'))
                print('Mindestens eine Datei ist keine pdf. Bitte wiederholen Sie die Eingabe.')
                self.filepaths_to_be_printed = []
                self.progress_bar['Value'] = 0
                self.label_files_text.set(InputInformation.get_folder_drop_init())
                return
            
            elif not os.path.exists(filepath):
                messagebox.showerror("Fehler",InputInformation.get_error_msg('none_existing_path'))
                status_text.set(InputInformation.get_status_text('process_canceled'))
                print('Mindestens ein Pfad zu einer Datei existiert nicht. Bitte wiederholen Sie die Eingabe.')
                self.filepaths_to_be_printed = []
                self.progress_bar['Value'] = 0
                self.label_files_text.set(InputInformation.get_folder_drop_init())
                return

        status_text.set(InputInformation.get_status_text('read_files_successful'))
        print(f'Dateien der Dateienliste eingelesen')    


    def plan_to_print_folder(self, folder_path, progress_bar, label_folder_text, status_text):
        self.progress_bar = progress_bar
        self.label_folder_text = label_folder_text
        
        for file in os.listdir(folder_path):
            filepath = os.path.join(folder_path, file)
            if os.path.isfile(filepath) and filepath.lower().endswith(".pdf") and os.path.exists(filepath):
                filepath = os.path.join(folder_path, file)
                self.filepaths_to_be_printed.append({"filepath": filepath, "copies": 1, "print": False})

            elif not os.path.isfile(os.path.join(folder_path, file)):
                messagebox.showerror("Fehler", InputInformation.get_error_msg('folder_consist_of_not_only_files'))
                status_text.set(InputInformation.get_status_text('process_canceled'))
                print('Die Eingegebenen Dateien sind nicht vom Typ Dateien. Bitte Wiederholen Sie die Eingabe.')
                # reset inputs
                self.filepaths_to_be_printed = []
                self.progress_bar['Value'] = 0
                self.label_folder_text.set(InputInformation.get_folder_drop_init())
                return

            elif not filepath.lower().endswith(".pdf"):
                messagebox.showerror("Fehler", InputInformation.get_error_msg('no_pdf_file_in_files'))
                status_text.set(InputInformation.get_status_text('process_canceled'))
                print('Mindestens eine Datei ist keine pdf. Bitte wiederholen Sie die Eingabe.')
                self.filepaths_to_be_printed = []
                self.progress_bar['Value'] = 0
                self.label_folder_text.set(InputInformation.get_folder_drop_init())
                return
            
            elif not os.path.exists(filepath):
                messagebox.showerror("Fehler", InputInformation.get_error_msg('none_existing_path'))
                status_text.set(InputInformation.get_status_text('process_canceled'))
                print('Mindestens ein Pfad zu einer Datei existiert nicht. Bitte wiederholen Sie die Eingabe.')
                self.filepaths_to_be_printed = []
                self.progress_bar['Value'] = 0
                self.label_folder_text.set(text=InputInformation.get_folder_drop_init())
                return

        status_text.set(InputInformation.get_status_text('read_files_successful'))
        print(f'Dateien des Ordners eingelesen')


    def print_input(self, status_text):
        
        if len(self.filepaths_to_be_printed) > 0:
            cnt_files = len(self.filepaths_to_be_printed)
            cnt_printed = 0
            for idx, file in enumerate(self.filepaths_to_be_printed, 1):
                
                if file["print_val"].get():
                    if file["copies_entry"].get().isdigit():
                        for i in range(int(file["copies_entry"].get())):
                            # print file
                            subprocess.run([self.ghostscript_path, 
                                            "-dBATCH",     # Batch-modus, no user iteractions
                                            "-dNOPAUSE",   # no pause between sites
                                            "-dQUIET",     # Keine Ausgaben in der Konsole
                                            "-sDEVICE=mswinpr2",  # Windows printer
                                            f"-sOutputFile=%printer%{self.printer}",  # set printer-name
                                            file["filepath"]], shell=True)
                            cnt_printed += cnt_printed
                    else:
                        messagebox.showinfo("Fehler", f"Die Datei: {file['filepath']} konnte nicht gedruckt werden da der Eintrag für die Anzahl der Kopien keine Zahl enthält.")

                # Fortschrittsbalken aktualisieren
                self.progress_bar['value'] = (idx / cnt_files) * 100
                if self.label_folder_text is not None:
                    self.label_folder_text.set(f"{idx}/{cnt_files} Dateien verarbeitet...")
                if self.label_files_text is not None:
                    self.label_files_text.set(f"{idx}/{cnt_files} Dateien verarbeitet...")

                status_text.set(f"Drucke {file['filepath']} auf {self.printer}...")
                print(f"Drucke {file['filepath']} auf {self.printer}...")
                time.sleep(0.1)

            status_text.set(f"{cnt_printed} von {cnt_files} Dateien gedruckt")
            print(f"{cnt_printed} von {cnt_files} Dateien gedruckt")
            self.filepaths_to_be_printed = []

        else:
            status_text.set(InputInformation.get_status_text('init'))
            messagebox.showinfo("Hinweis" ,"Es sing keine Dateien ausgewählt.")
            print('Es sing keine Dateien ausgewählt.')