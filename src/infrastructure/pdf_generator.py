'''Module to create PDFs'''
from fpdf import FPDF
from infrastructure.file_manager import FileDownloader
from feature.image_converter.image_converter_interfaces import IImageEditorService
from configs.my_logger import get_logger

class PdfCreator:
    '''Class to handle pdf creation'''
    def __init__(
        self,
        folder:FileDownloader,
        pdf_name:str,
        image_editor: IImageEditorService
    ) -> None:
        self.folder = folder
        self.pdf_name = pdf_name
        self.image_editor = image_editor
        self._logger = get_logger(__name__)

    def create_pdf(self, manga_data: dict[str,str] | None):
        self._logger.info(
            "Start process to create [%s] pdf from folder[%s]", 
            self.pdf_name,
            self.folder.folder_path)
        pdf = FPDF(unit= "pt")
        for image in self.folder.get_images_in_folder():
            self._logger.info("Add page of image %s", image)
            image_path = f"{self.folder.folder_path}/{image}"
            pdf.add_page(
                "P",
                self.image_editor.get_image_size(self.folder, image),
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
                pdf.set_font("Arial", "", 10)
                pdf.write(10, data)


        self._logger.info("Saving PDF %s", self.pdf_name)
        pdf.output(f"{self.folder.folder_path}/{self.pdf_name}")
        self._logger.info("PDF created [%s]", self.pdf_name)
        return
