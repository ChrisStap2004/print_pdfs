import os
import subprocess
import win32print
import time
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD, DND_FILES


# requirements for application:
#   - download ghostscript


# tickets:
#   Settings-Window:
#   - window that allows selecting printer ++++++
#   - 



def print_files(files_list, progress_bar, label):
    
    # requirements
    acrobat_path = r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe" 
    printer = win32print.GetDefaultPrinter()
    ghostscript_path = r"C:\Program Files\gs\gs10.04.0\bin\gswin64c.exe"

    cnt_files = len(files_list)

    for index, file_path in enumerate(files_list, 0):
        orig_dateipfad = file_path

        # Überprüfen, ob die Datei existiert und ob es eine PDF-Datei ist
        if os.path.exists(orig_dateipfad) and orig_dateipfad.lower().endswith(".pdf"):
            print(f"Drucke {orig_dateipfad} auf {printer}...")
            # Subprozess zum Drucken der PDF-Datei mit Ghostscript
            subprocess.run([ghostscript_path, 
                            "-dBATCH",     # Batch-Modus, keine Benutzerinteraktion
                            "-dNOPAUSE",   # Keine Pause zwischen den Seiten
                            "-dQUIET",     # Keine Ausgaben in der Konsole
                            "-sDEVICE=mswinpr2",  # Windows Drucker
                            f"-sOutputFile=%printer%{printer}",  # Druckername
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




def print_folder(folder_path, progress_bar, label):
    
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # requirements
    acrobat_path = r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe" 
    printer = win32print.GetDefaultPrinter()
    ghostscript_path = r"C:\Program Files\gs\gs10.04.0\bin\gswin64c.exe"


    cnt_files = len(files)

    for index, file in enumerate(files, 1):  # Index für Fortschritt verwenden
        orig_dateipfad = os.path.join(folder_path, file)
        
        # Überprüfen, ob die Datei existiert und ob es eine PDF-Datei ist
        if os.path.exists(orig_dateipfad) and orig_dateipfad.lower().endswith(".pdf"):
            print(f"Drucke {orig_dateipfad} auf {printer}...")
            # Subprozess zum Drucken der PDF-Datei mit Ghostscript
            subprocess.run([ghostscript_path, 
                            "-dBATCH",     # Batch-Modus, keine Benutzerinteraktion
                            "-dNOPAUSE",   # Keine Pause zwischen den Seiten
                            "-dQUIET",     # Keine Ausgaben in der Konsole
                            "-sDEVICE=mswinpr2",  # Windows Drucker
                            f"-sOutputFile=%printer%{printer}",  # Druckername
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



def create_gui():

    # create main-window
    root = TkinterDnD.Tk()
    root.title("Drucken von PDF in Eingabeform von Dateien oder Ordner")
    root.geometry("800x400")
    root.grid_rowconfigure(0, weight=5)
    root.grid_rowconfigure(1, weight=0)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # create sub-windows: file, folder, bar
    folder_frame = tk.Frame(root, width=400, height=300, bd=2, relief='groove')
    folder_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    files_frame = tk.Frame(root, width=400, height=300, bd=2, relief='groove')
    files_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

    bar_frame = tk.Frame(root, width=400, height=100, bd=2, relief='groove')
    bar_frame.grid(row=1, columnspan=2, padx=5, pady=5, sticky='nsew')


    # labels for windows
    label_folder = tk.Label(folder_frame, text="Ziehen Sie einen Ordner hierher, um die PDFs zu drucken.", padx=10, pady=10)
    label_folder.pack(fill='both', expand=True, padx=20, pady=20)

    label_files = tk.Label(files_frame, text="Ziehen Sie versch. Dateien hierher, um die PDFs zu drucken.", padx=10, pady=10)
    label_files.pack(fill='both', expand=True, padx=20, pady=20)

    # Fortschrittsbalken erstellen
    progress_bar = ttk.Progressbar(bar_frame, orient="horizontal", length=400, mode="determinate")
    progress_bar.pack(pady=20)



    # drag and drop of folder
    def on_left_drop(event):
        ordnerpfad = event.data.strip('{}')  # Der Ordnerpfad, der vom Benutzer gezogen wurde
        # check data_format
        if not os.path.isdir(ordnerpfad):
            print("Sie haben keinen Ordner abgelegt. Bitte wiederholen")
            exit
        
        print(f"Ordner ausgewählt: {ordnerpfad}")
        # Fortschrittsbalken auf 0 setzen
        progress_bar['value'] = 0
        label_folder.config(text="Druckvorgang läuft...")
        # Dateien drucken
        print_folder(ordnerpfad,  progress_bar, label_folder)


    # drag and drop of files
    def on_right_drop(event):
            files_list = event.data.split('} {')  # Der Pfad der Datei, die auf das rechte Drop-Ziel gezogen wurde
            all_files_and_pdfs = True
            for i in range(len(files_list)):
                files_list[i] = files_list[i].strip('{').strip('}')
                if not (os.path.isfile(files_list[i]) and files_list[i].lower().endswith(".pdf")):
                    all_files_and_pdfs = False
                    break
            if all_files_and_pdfs:
                print(f"Dateien ausgewählt: {files_list}")
                # Fortschrittsbalken auf 0 setzen und die Datei drucken
                progress_bar['value'] = 0
                label_files.config(text="Druckvorgang läuft...")
                print_files(files_list, progress_bar, label_files)
            else:
                print("Erwarteter Datentyp .pdf nicht bei allen Dateien vorhanden.")


    # Drag & Drop auf das Fenster ermöglichen
    folder_frame.drop_target_register(DND_FILES)
    folder_frame.dnd_bind('<<Drop>>', on_left_drop)

    files_frame.drop_target_register(DND_FILES)
    files_frame.dnd_bind('<<Drop>>', on_right_drop)


    # Starten der GUI
    root.mainloop()

# Starte die GUI
create_gui()

# Beispielaufruf
#ordner = r"C:\Users\cohen\OneDrive\PC Workspace\Dokumente\Henriette_Haase\Jette_Rechnungen_drucken"
#print_files(ordner)
