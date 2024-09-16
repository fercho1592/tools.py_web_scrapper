from . import image_converter_interfaces
from infrastructure.file_manager import FileDownloader
from configs.my_logger import get_logger
from PIL import Image

class PillowImageConverter(image_converter_interfaces.IImageConverter):
  def __init__(self, folder_manager:FileDownloader) -> None:
    self.folder_manager = folder_manager
    self._logger = get_logger(__name__)
    pass

  def convert_image(
      self,
      image: str,
      new_image_name,
      dest_path="./converted_to_jpg"
    ):
    folder_path = self.folder_manager.folder_path
    old_image_path = f"{folder_path}/{image}"
    new_image_path = f"{folder_path}/{dest_path}/{new_image_name}"

    try:
      img = Image.open(old_image_path)
      img.save(new_image_path, "PNG")
      self._logger.info("Imagen convertida: %s", new_image_path)
    except FileNotFoundError:
      self._logger.error("No se encontró el archivo: %s", old_image_path)
    except OSError as e:
      print("Error al convertir la imagen %s | %r",image, e)
