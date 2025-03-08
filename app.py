from pdf_printer_app import PDFPrinterApp
from printer_manager import PrinterManager
from pdf_processor import PDFProcessor

def main():
    printer_manager = PrinterManager()
    pdf_processor = PDFProcessor(printer_manager)
    
    app = PDFPrinterApp(printer_manager, pdf_processor)
    app.run()

if __name__ == "__main__":
    main()