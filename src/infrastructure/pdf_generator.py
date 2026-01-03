'''Module to create PDFs'''
from fpdf import FPDF
from feature_interfaces.services.file_manager import IFileScrapperManager
from feature_interfaces.services.pdf_creator import IPdfCreator
from feature.image_converter.image_converter_interfaces import IImageEditorService
from tools.string_path_fix import FixStringsTools
from feature_interfaces.protocols.config_protocol import LoggerProtocol

class PdfCreator(IPdfCreator):
    def __init__(
        self,
        folder: IFileScrapperManager,
        imageEditor: IImageEditorService,
        logger: LoggerProtocol
    ) -> None:
        self.FileManager = folder
        self.ImageEditor = imageEditor
        self._logger = logger
    
    def CreatePdf(self, pdfName: str, manga_data: dict[str,str] | None):
        self._logger.info(
            "Start process to create [%s] pdf from folder[%s]", 
            pdfName,
            self.FileManager.GetFolderPath())
        pdf = FPDF(unit= "pt")
        pdf.add_font("Swansea", "", "Swansea-q3pd.ttf")
        pdf.set_font("Swansea","", 10)
        for image in self.FileManager.GetImagesInFolder():
            self._logger.info("Add page of image %s", image)
            image_path = f"{self.FileManager.GetFolderPath()}/{image}"
            pdf.add_page(
                "P",
                self.ImageEditor.get_image_size(self.FileManager, image),
                False
            )
            pdf.image(image_path, x=0, y=0)

        if manga_data is not None:
            self._logger.info("Add data page %s", manga_data)
            pdf.add_page("P", "A4", False)
            pdf.set_font("Arial", "", 10)
            pdf.set_margins(24.5, 34.65, 24.5)
            for (key, data) in manga_data.items():
                pdf.ln(10)
                pdf.set_font("Arial", "B", 12)
                pdf.write(10, key)
                pdf.ln(10)
                pdf.set_font("Swansea","", 10)
                pdf.write(10, FixStringsTools.NormalizeString(data),)


        self._logger.info("Saving PDF %s", pdfName)
        pdf.output(f"{self.FileManager.GetFolderPath()}/{pdfName}")
        self._logger.info("PDF created [%s]", pdfName)
        return

    def SetFileManager(self, fileManager):
        self.FileManager = fileManager
