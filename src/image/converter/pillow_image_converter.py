from image.converter.image_converter_interfaces import IImageEditorService
from core.services.file_manager import FileManager
from contracts.models.folders_struct import FolderPath
from contracts.protocols.config_protocol import LoggerProtocol
from PIL import Image

# IMAGE_FORMAT = "JPEG"
IMAGE_FORMAT = "PNG"


class PillowImageConverter(IImageEditorService):
    def __init__(self, logger: LoggerProtocol) -> None:
        self._logger = logger
        pass

    def convert_image(
        self,
        folder_manager: FolderPath,
        image_name: str,
        new_image_name: str,
        destinyFolder: FolderPath,
    ):
        fileManager = FileManager(self._logger)
        new_image_name = f"{new_image_name}.{IMAGE_FORMAT.lower()}"

        if fileManager.HasFile(destinyFolder, new_image_name):
            self._logger.info("Image duplicated: %s", new_image_name)
            return

        try:
            with Image.open(folder_manager.get_file_path(image_name)) as img:
                convertedImage = Image.new("RGBA", img.size)
                convertedImage.paste(img)
                convertedImage.save(
                    destinyFolder.get_file_path(new_image_name), IMAGE_FORMAT
                )
            self._logger.info("Image converted: %s", new_image_name)
        except FileNotFoundError as e:
            self._logger.error(
                "File not found: %s | %r", folder_manager.get_file_path(image_name), e
            )
        except OSError as e:
            self._logger.error("Error al convertir la imagen %s | %r", image_name, e)
        return

    def get_image_size(
        self,
        folder_manager: FolderPath,
        image_name: str,
    ):
        image_path = folder_manager.get_file_path(image_name)
        with Image.open(image_path) as img:
            size = img.size
            self._logger.debug("Get image size of: %s", size)
            result_size = (float(size[0]), float(size[1]))
            self._logger.debug("Result image size of: %s", result_size)
            return result_size
