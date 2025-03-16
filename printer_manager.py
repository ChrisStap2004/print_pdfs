import win32print
import subprocess


class PrinterManager:
    def __init__(self):
        self.printers = self.get_printers()
        self.selected_printer = win32print.GetDefaultPrinter()
        self.process = None

    def get_printers(self):
        return [printer[2] for printer in win32print.EnumPrinters(2)]
    
    def set_printer(self, printer_name):
        self.selected_printer = printer_name
        print(f'Drucker ausgewählt: {printer_name}')

    def get_selected_printer(self):
        return self.selected_printer
    
    def open_printing_queue(self):
        try:
            self.process = subprocess.Popen(f'rundll32 printui.dll,PrintUIEntry /o /n"{self.selected_printer}"',
                                            shell=True,
                                        )
        except Exception as e:
            print(f"Fehler beim Öffnen der Druckerwarteschlange: {e}")

    def close_printing_queue(self):
        if self.process and self.process.poll() is None:    # if process still running
            subprocess.run("wmic process where \"name='printui.exe'\" call terminate", shell=True)