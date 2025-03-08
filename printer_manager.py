import win32print


class PrinterManager:
    def __init__(self):
        self.printers = self.get_printers()
        self.selected_printer = None

    def get_printers(self):
        return [printer[2] for printer in win32print.EnumPrinters(2)]
    
    def set_printer(self, printer_name):
        self.selected_printer = printer_name
        print(f'Drucker ausgewählt: {printer_name}')

    def get_selected_printer(self):
        return self.selected_printer