from dataclasses import dataclass
from configs.logger_factory import LoggerFactory
from feature.image_converter.image_converter_interfaces import IImageEditorService
from feature.services.file_manager import FileManager
from feature_interfaces.models.folders_struct import FolderPath


@dataclass
class ImageConverterCommand:
    image_folder: FolderPath
    pdf_folder: FolderPath


class ImageConverterHandler:
    def __init__(
        self, logger_factory: LoggerFactory, image_converter: IImageEditorService
    ):
        self._logger = logger_factory.get_logger(__name__)
        self._image_converter = image_converter

    async def handle(self, command: ImageConverterCommand) -> None:
        fileManager = FileManager(self._logger)
        fileManager.CreateIfNotexist(command.pdf_folder)
        try:
            self._logger.info("Start Convert Images")
            for image_name in fileManager.GetImagesInFolder(command.image_folder):
                splited_name = image_name.split(".")
                if splited_name[-1].upper() not in ["PNG", "JPG"]:
                    self._image_converter.convert_image(
                        command.image_folder,
                        image_name,
                        splited_name[0],
                        command.pdf_folder,
                    )
                else:
                    fileManager.MoveFileTo(
                        command.image_folder, image_name, command.pdf_folder
                    )

            fileManager.DeleteAll(command.image_folder)
        finally:
            self._logger.info("End Convert Images")
