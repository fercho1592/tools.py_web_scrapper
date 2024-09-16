from fpdf import FPDF
from infrastructure.file_manager import FileDownloader
from infrastructure.my_logger import get_logger

class PdfCreator:
  def __init__(self, folder:FileDownloader, pdf_name:str) -> None:
    self.folder = folder
    self.pdf_name = pdf_name
    self._logger = get_logger(__name__)

  def create_pdf(self):
    self._logger.debug("Start process to create %s pdf", self.pdf_name)
    pdf = FPDF()
    for image in self.folder.get_images_in_folder():
      pdf.add_page()
      pdf.image(f"{self.folder.folder_path}/{image}", x=0, y=0)
    pdf.output(f"{self.folder.folder_path}/{self.pdf_name}", )
