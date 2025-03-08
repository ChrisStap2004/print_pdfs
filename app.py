from pdf_printer_app import PDFPrinterApp
from printer_manager import PrinterManager

def main():
    printer_manager = PrinterManager()
    app = PDFPrinterApp(printer_manager=printer_manager)
    app.run()

if __name__ == "__main__":
    main()