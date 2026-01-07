'''Module to create PDFs'''
from fpdf import FPDF
from feature.services.file_manager import FileManager
from feature.image_converter.image_converter_interfaces import IImageEditorService
from feature_interfaces.models.folders_struct import FolderPath
from feature_interfaces.services.pdf_creator import IPdfCreator
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from tools.string_path_fix import FixStringsTools

class PdfCreator(IPdfCreator):
    def __init__(
        self,
        imageEditor: IImageEditorService,
        logger: LoggerProtocol
    ) -> None:
        self.ImageEditor = imageEditor
        self._logger = logger
    
    def CreatePdf(self, pdfName: str, manga_data: dict[str,str] | None, imageFolder: FolderPath, resultFolder: FolderPath) -> None:
        self._logger.info(
            "Start process to create [%s] pdf from folder[%s]", 
            pdfName,
            resultFolder.relative_path)
        pdf_creator = self.init_pdf_creator()
        fileManager = FileManager(self._logger)

        for image in fileManager.GetImagesInFolder(imageFolder):
            self._logger.info("Add page of image %s", image)
            image_path = imageFolder.get_file_path(image)
            pdf_creator.add_page(
                "P",
                self.ImageEditor.get_image_size(imageFolder, image),
                False
            )
            pdf_creator.image(image_path, x=0, y=0)

        self.add_metadata_to_pdf(pdf_creator, manga_data)
        self._logger.info("Saving PDF %s", pdfName)

        pdf_creator.output(resultFolder.get_file_path(pdfName))
        self._logger.info("PDF created [%s]", pdfName)
        return

    def SetFileManager(self, fileManager):
        self.FileManager = fileManager

    def init_pdf_creator(self) -> FPDF:
        pdf = FPDF(unit= "pt")
        pdf.add_font("Swansea", "", "Swansea-q3pd.ttf")
        pdf.set_font("Swansea","", 10)

        return pdf
    
    def add_metadata_to_pdf(self, pdf: FPDF, manga_data: dict[str,str] | None) -> None:
        if manga_data is None:
            return
        
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
