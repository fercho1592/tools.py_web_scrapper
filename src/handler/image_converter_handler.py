from dataclasses import dataclass
from feature.image_converter.image_converter_interfaces import IImageEditorService
from feature.services.file_manager import FileManager
from feature_interfaces.models.folders_struct import FolderPath
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from wrappers.handler_decorators import log_ejecucion


@dataclass
class ImageConverterCommand:
    image_folder: FolderPath
    pdf_folder: FolderPath


@log_ejecucion
async def handle(
    fileManager: FileManager,
    logger: LoggerProtocol,
    image_converter: IImageEditorService,
    command: ImageConverterCommand,
) -> None:
    fileManager.CreateIfNotexist(command.pdf_folder)
    for image_name in fileManager.GetImagesInFolder(command.image_folder):
        splited_name = image_name.split(".")
        if splited_name[-1].upper() not in ["PNG", "JPG"]:
            logger.info(f"Converting image: {image_name}")
            image_converter.convert_image(
                command.image_folder,
                image_name,
                splited_name[0],
                command.pdf_folder,
            )
        else:
            fileManager.MoveFileTo(command.image_folder, image_name, command.pdf_folder)
