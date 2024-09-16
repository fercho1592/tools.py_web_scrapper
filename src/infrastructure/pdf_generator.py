from fpdf import FPDF
from infrastructure.file_manager import FileDownloader
from feature.image_converter.image_converter_interfaces import IImageEditorService
from configs.my_logger import get_logger

class PdfCreator:
  def __init__(self, folder:FileDownloader, pdf_name:str, image_editor: IImageEditorService) -> None:
    self.folder = folder
    self.pdf_name = pdf_name
    self.image_editor = image_editor
    self._logger = get_logger(__name__)

  def create_pdf(self):
    self._logger.debug("Start process to create %s pdf", self.pdf_name)
    pdf = FPDF(unit= "pt")
    for image in self.folder.get_images_in_folder():
      image_path = f"{self.folder.folder_path}/{image}"
      pdf.add_page("P", self.image_editor.get_image_size(self.folder, image), False)
      pdf.image(image_path, x=0, y=0)
    pdf.output(f"{self.folder.folder_path}/{self.pdf_name}")
    return
