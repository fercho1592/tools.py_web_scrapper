from . import image_converter_interfaces
from infrastructure.file_manager import FileDownloader
from configs.my_logger import get_logger
from PIL import Image

IMAGE_FORMAT = "JPEG"

class PillowImageConverter(image_converter_interfaces.IImageEditorService):
  def __init__(self) -> None:
    self._logger = get_logger(__name__)
    pass

  def convert_image(
      self,
      folder_manager: FileDownloader,
      image_name: str,
      new_image_name,
      dest_path="converted_to_png"
    ):
    new_image_name = f"{new_image_name}.{IMAGE_FORMAT.lower()}"
    folder_path = folder_manager.folder_path
    old_image_path = f"{folder_path}/{image_name}"
    new_folder_path =f"{folder_path}/{dest_path}" 
    new_image_path = f"{new_folder_path}/{new_image_name}"
    folder_manager.create_folder_if_not_exist(new_folder_path)
    if folder_manager.exist_file(new_image_path):
      self._logger.info("Image duplicated: %s", new_image_name)
      return

    try:
      img = Image.open(old_image_path)
      img.save(new_image_path, IMAGE_FORMAT)
      self._logger.info("Image converted: %s", new_image_name)
    except FileNotFoundError as e:
      self._logger.error("File not found: %s | %r", old_image_path, e)
    except OSError as e:
      self._logger.error("Error al convertir la imagen %s | %r", image_name, e)

  def get_image_size(
    self,
    folder_manager:FileDownloader,
    image_name: str
  ):
    image_path = f"{folder_manager.folder_path}/{image_name}"
    img = Image.open(image_path)
    size = img.size
    self._logger.debug("Get image size of: %s", size)
    result_size = (float(size[0]), float(size[1]))
    self._logger.debug("Result image size of: %s", result_size)
    return result_size
