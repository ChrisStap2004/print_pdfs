import win32print
import subprocess


class PrinterManager:
    def __init__(self):
        self.printers = self.get_printers()
        self.selected_printer = win32print.GetDefaultPrinter()
        self.process = None

    def get_printers(self):
        return [printer[2] for printer in win32print.EnumPrinters(2)]
    
    def set_printer(self, printer_name, status_text):
        self.selected_printer = printer_name
        status_text.set(f"Ausgewählter Drucker: {printer_name}")
        print(f'chosen printer: {printer_name}')

    def get_selected_printer(self):
        return self.selected_printer
    
    def open_printing_queue(self, status_text):
        try:
            self.process = subprocess.Popen(f'rundll32 printui.dll,PrintUIEntry /o /n"{self.selected_printer}"',
                                            shell=True,
                                        )
            status_text.set("Druckerwarteschlange geöffnet.")
        except Exception as e:
            print(f"Error at opening printing-queue {e}")

    # not working properly but not needed tbh
    def close_printing_queue(self):         
        if self.process and self.process.poll() is None:    # if process still running
            subprocess.run("wmic process where \"name='printui.exe'\" call terminate", shell=True)