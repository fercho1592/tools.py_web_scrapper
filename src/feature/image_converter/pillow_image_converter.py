from .image_converter_interfaces import IImageEditorService
from feature_interfaces.services.file_manager import IFileManager
from configs.my_logger import get_logger
from PIL import Image

#IMAGE_FORMAT = "JPEG"
IMAGE_FORMAT = "PNG"

class PillowImageConverter(IImageEditorService):
    def __init__(self) -> None:
        self._logger = get_logger(__name__)
        pass

    def convert_image(
        self,
        folder_manager: IFileManager,
        image_name: str,
        new_image_name: str,
        destinyFolder: IFileManager
    ):
        new_image_name = f"{new_image_name}.{IMAGE_FORMAT.lower()}"

        if folder_manager.HasFile(new_image_name):
            self._logger.info("Image duplicated: %s", new_image_name)
            return

        try:
            img = Image.open(folder_manager.GetFilePath(image_name))
            convertedImage = Image.new("RGBA", img.size)
            convertedImage.paste(img)
            convertedImage.save(destinyFolder.GetFilePath(new_image_name), IMAGE_FORMAT)
            self._logger.info("Image converted: %s", new_image_name)
        except FileNotFoundError as e:
            self._logger.error("File not found: %s | %r", folder_manager.GetFilePath(image_name), e)
        except OSError as e:
            self._logger.error("Error al convertir la imagen %s | %r", image_name, e)
        return

    def get_image_size(
        self,
        folder_manager:IFileManager,
        image_name: str
    ):
        image_path = f"{folder_manager.GetFolderPath()}/{image_name}"
        img = Image.open(image_path)
        size = img.size
        self._logger.debug("Get image size of: %s", size)
        result_size = (float(size[0]), float(size[1]))
        self._logger.debug("Result image size of: %s", result_size)
        return result_size
