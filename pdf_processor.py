import time
import win32print
import subprocess
import os
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD, DND_FILES

# subclasses
from pdf_printer_app import PDFPrinterApp



class PDFProcessor(PDFPrinterApp):
    def __init__(self):
        # inherit attributes from PDFPrinterApp (includes printer_manager)
        super().__init__()

        # initialize scripts
        self.acrobat_path = r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe" 
        self.printer = self.printer_manager.get_selected_printer()
        self.ghostscript_path = r"C:\Program Files\gs\gs10.04.0\bin\gswin64c.exe"


    def print_files(self, files_list, progress_bar, label):

        cnt_files = len(files_list)

        for index, file_path in enumerate(files_list, 0):
            orig_dateipfad = file_path

            # Überprüfen, ob die Datei existiert und ob es eine PDF-Datei ist
            if os.path.exists(orig_dateipfad) and orig_dateipfad.lower().endswith(".pdf"):
                print(f"Drucke {orig_dateipfad} auf {self.printer}...")
                # Subprozess zum Drucken der PDF-Datei mit Ghostscript
                subprocess.run([self.ghostscript_path, 
                                "-dBATCH",     # Batch-Modus, keine Benutzerinteraktion
                                "-dNOPAUSE",   # Keine Pause zwischen den Seiten
                                "-dQUIET",     # Keine Ausgaben in der Konsole
                                "-sDEVICE=mswinpr2",  # Windows Drucker
                                f"-sOutputFile=%printer%{self.printer}",  # Druckername
                                orig_dateipfad], shell=True)
                
                # Fortschrittsbalken aktualisieren
                progress_bar['value'] = (index + 1 / cnt_files) * 100
                label.config(text=f"{index + 1}/{cnt_files} Dateien verarbeitet...")
                label.update_idletasks()  # UI aktualisieren

                time.sleep(0.5)
            else:
                print(f"Datei: {orig_dateipfad} nicht gefunden oder keine PDF...")

        # Nachdem alle Dateien verarbeitet sind, Fortschritt auf 100% setzen
        progress_bar['value'] = 100
        label.config(text=f"Alle {cnt_files} Dateien wurden gedruckt!")




    def print_folder(self, folder_path, progress_bar, label):
        
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        cnt_files = len(files)

        for index, file in enumerate(files, 1):  # Index für Fortschritt verwenden
            orig_dateipfad = os.path.join(folder_path, file)
            
            # Überprüfen, ob die Datei existiert und ob es eine PDF-Datei ist
            if os.path.exists(orig_dateipfad) and orig_dateipfad.lower().endswith(".pdf"):
                print(f"Drucke {orig_dateipfad} auf {self.printer}...")
                # Subprozess zum Drucken der PDF-Datei mit Ghostscript
                subprocess.run([self.ghostscript_path, 
                                "-dBATCH",     # Batch-Modus, keine Benutzerinteraktion
                                "-dNOPAUSE",   # Keine Pause zwischen den Seiten
                                "-dQUIET",     # Keine Ausgaben in der Konsole
                                "-sDEVICE=mswinpr2",  # Windows Drucker
                                f"-sOutputFile=%printer%{self.printer}",  # Druckername
                                orig_dateipfad], shell=True)
                
                # Fortschrittsbalken aktualisieren
                progress_bar['value'] = (index / cnt_files) * 100
                label.config(text=f"{index}/{cnt_files} Dateien verarbeitet...")
                label.update_idletasks()  # UI aktualisieren

                time.sleep(0.5)
            else:
                print(f"Datei: {orig_dateipfad} nicht gefunden oder keine PDF...")

        # Nachdem alle Dateien verarbeitet sind, Fortschritt auf 100% setzen
        progress_bar['value'] = 100
        label.config(text=f"Alle {cnt_files} Dateien wurden gedruckt!")