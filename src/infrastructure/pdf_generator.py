from imagekitio import ImageKit
from infrastructure.file_downloader import FileDownloader
from infrastructure.my_logger import get_logger

class PdfCreator:
  def __init__(self, folder:FileDownloader, pdf_name:str) -> None:
    self.folder = folder
    self.pdf_name = pdf_name
    self._logger = get_logger(__name__)

  def create_pdf(self):
    self._logger.debug("Start process to create %s pdf", self.pdf_name)
    images = self.folder.get_images_in_folder()
    # Crear un objeto ImageKit
    ik = ImageKit()
    # Convertir las imágenes a PDF
    ik.pdf_from_images(images, output_file=f"{self.folder}/{self.pdf_name}")
