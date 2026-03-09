from dataclasses import dataclass
from wrappers.handler_decorators import log_ejecucion
from feature_interfaces.models.folders_struct import FolderPath
from feature_interfaces.services.pdf_creator import IPdfCreator


@dataclass
class PDFCreatorCommand:
    image_folder: FolderPath
    pdf_folder: FolderPath
    pdf_name: str
    manga_data: dict[str, str]


@DeprecationWarning(
    "Use the handle function instead of the class-based handler for better performance and simplicity."
)
class PDFCreatorHandler:
    def __init__(self, pdf_creator_service: IPdfCreator):
        self._pdf_creator = pdf_creator_service

    @log_ejecucion
    async def handle(self, command: PDFCreatorCommand) -> None:
        self._pdf_creator.CreatePdf(
            command.pdf_name,
            command.manga_data,
            command.image_folder,
            command.pdf_folder,
        )


@log_ejecucion
async def handle(pdf_creator_service: IPdfCreator, command: PDFCreatorCommand) -> None:
    pdf_creator_service.CreatePdf(
        command.pdf_name,
        command.manga_data,
        command.image_folder,
        command.pdf_folder,
    )
