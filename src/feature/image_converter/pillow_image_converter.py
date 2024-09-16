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
      image_name: str,
      new_image_name,
      dest_path="converted_to_png"
    ):
    folder_path = self.folder_manager.folder_path
    old_image_path = f"{folder_path}/{image_name}"
    new_folder_path =f"{folder_path}/{dest_path}" 
    new_image_path = f"{new_folder_path}/{new_image_name}"
    self.folder_manager.create_folder_if_not_exist(new_folder_path)
    if self.folder_manager.exist_file(new_image_path):
      self._logger.info("Image duplicated: %s", new_image_name)
      return

    try:
      img = Image.open(old_image_path)
      img.save(new_image_path, "PNG")
      self._logger.info("Image converted: %s", new_image_name)
    except FileNotFoundError as e:
      self._logger.error("File not found: %s | %r", old_image_path, e)
    except OSError as e:
      self._logger.error("Error al convertir la imagen %s | %r", image_name, e)
