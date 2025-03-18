class InputInformation:

    FOLDER_DROP_INIT = "Ziehen Sie einen Ordner hierher, um die PDFs zu drucken."
    FILES_DROP_INIT = "Ziehen Sie versch. Dateien hierher, um die PDFs zu drucken."
    PRINTING = "Druckvorgang läuft ..."

    ROOT_TITLE = "Drucken von PDF in Eingabeform von Dateien oder Ordner"
    ROOT_GEOMETRIE = "1000x500"

    OVERVIEW_GEOMETRIE = "1200x600"
    OV_HEADER_LABELS = ["Dateiname", "Anzahl an Kopien", "Drucken"]

    # status-row-text
    STATUS = {
        'init': "Bereit",
        'print_canceled': "Druckvorgang abgebrochen. Bereit für neue Eingabe.",
        'process_canceled': "Vorgang abgebrochen. Bereit für neue Eingabe.",
        'read_files_successful': "Dateien erfolgreich eingelesen.",
        'all_files_printed': "Alle Dateien wurden erfolgreich gedruckt."
    }

    # error-messages
    ERROR = {
        'no_folder_dropped': "Kein Ordner wurde abgelegt. Wiederholen Sie den Vorgang.",
        'no_files_to_print': "Keine Dateien wurden zum Drucken hinzugefügt.",
        'no_pdf_file_in_files': "Mindestens eine Datei ist keine pdf. Bitte wiederholen Sie die Eingabe.",
        'none_existing_path': "Mindestens ein Pfad zu einer Datei existiert nicht. Bitte wiederholen Sie die Eingabe.",
        'folder_consist_of_not_only_files': "Mindestens eine Datei des Ordners ist nicht vom Typ Datei. Bitte Wiederholen Sie die Eingabe."
    }   

    @staticmethod
    def get_ghostscript_path():
        return r"C:\Program Files\gs\gs10.04.0\bin\gswin64c.exe"


    @staticmethod
    def get_folder_drop_init():
        return InputInformation.FOLDER_DROP_INIT
    
    @staticmethod
    def get_files_drop_init():
        return InputInformation.FILES_DROP_INIT
    
    @staticmethod
    def get_printing():
        return InputInformation.PRINTING
    
    @staticmethod
    def get_root_title():
        return InputInformation.ROOT_TITLE
    
    @staticmethod
    def get_root_geometrie():
        return InputInformation.ROOT_GEOMETRIE
    
    @staticmethod
    def get_overview_geometrie():
        return InputInformation.OVERVIEW_GEOMETRIE

    @staticmethod
    def get_overview_HEADER():
        return InputInformation.OV_HEADER_LABELS
    
    @staticmethod
    def get_status_text(key):
        return InputInformation.STATUS[key]
    
    @staticmethod
    def get_error_msg(key):
        return InputInformation.ERROR[key]