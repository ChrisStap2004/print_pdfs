class InputInformation:
    FOLDER_DROP_INIT = "Ziehen Sie einen Ordner hierher, um die PDFs zu drucken."
    FILES_DROP_INIT = "Ziehen Sie versch. Dateien hierher, um die PDFs zu drucken."
    PRINTING = "Druckvorgang läuft ..."

    ROOT_TITLE = "Drucken von PDF in Eingabeform von Dateien oder Ordner"
    ROOT_GEOMETRIE = "800x400"

    OVERVIEW_GEOMETRIE = "800x400"


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