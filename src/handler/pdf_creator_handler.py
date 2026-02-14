from dataclasses import dataclass
from feature_interfaces.models.folders_struct import FolderPath
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from feature_interfaces.services.pdf_creator import IPdfCreator


@dataclass
class PDFCreatorCommand:
    image_folder: FolderPath
    pdf_folder: FolderPath
    pdf_name: str
    manga_data: dict[str, str]


class PDFCreatorHandler:
    def __init__(
        self, logger_factory: LoggerProtocol, pdf_creator_service: IPdfCreator
    ):
        self._logger = logger_factory
        self._pdf_creator = pdf_creator_service

    async def handle(self, command: PDFCreatorCommand) -> None:
        try:
            self._logger.info("Start create PDF")
            self._pdf_creator.CreatePdf(
                command.pdf_name,
                command.manga_data,
                command.image_folder,
                command.pdf_folder,
            )
        finally:
            self._logger.info("End Create Pdf")
