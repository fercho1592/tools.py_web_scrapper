import asyncio
from dataclasses import dataclass
from threading import Thread

from contracts.models.folders_struct import FolderPath, MangaFoldersStruct
from contracts.protocols.queue_handler_protocol import (
    QueueHandlerProtocol,
    QueueMessage,
)
from core.services.error_handler import ErrorLogFileHandler


@dataclass
class PDFCreateQueueCommand:
    image_folder: FolderPath
    pdf_folder: FolderPath
    pdf_name: str
    manga_data: dict[str, str]
    queue_name: str = ""
    next_queue: str = ""


class PDFCreateQueueHandler(QueueHandlerProtocol[PDFCreateQueueCommand]):
    def __init__(
        self,
        queue_name: str,
        next_queue: str,
        file_manager,
        logger,
        error_handler,
        ui_handler,
        fn_pdf_creator_handler,
    ):
        self.file_manager = file_manager
        self.logger = logger
        self.error_handler = error_handler
        self.ui_handler = ui_handler
        self.fn_pdf_creator_handler = fn_pdf_creator_handler
        super().__init__(queue_name, next_queue)

    def on_message(self, command: QueueMessage[PDFCreateQueueCommand]):
        def process_pdf_creation():
            pdf_command = command.messageCommand
            folders = MangaFoldersStruct(pdf_command.pdf_name)
            error_handler = ErrorLogFileHandler(
                pdf_command.pdf_name,
                folders.error_log_folder,
            )
            self.error_handler = error_handler

            try:
                image_folder = pdf_command.image_folder
                pdf_folder = pdf_command.pdf_folder

                if not isinstance(image_folder, FolderPath):
                    raise TypeError("image_folder must be a FolderPath instance")
                if not isinstance(pdf_folder, FolderPath):
                    raise TypeError("pdf_folder must be a FolderPath instance")

                self.ui_handler.ShowMessage("Creating Pdf")
                result = self.fn_pdf_creator_handler(pdf_command)
                if asyncio.iscoroutine(result):
                    asyncio.run(result)

                self.ui_handler.ShowMessage("Deleting Convert Folder")
                self.file_manager.DeleteAll(image_folder)

                self.ui_handler.ShowMessage(
                    f"PDf created in [{pdf_folder.get_file_path(pdf_command.pdf_name)}]"
                )
                self.logger.info(
                    "PDF created for [%s] in [%s]",
                    pdf_command.pdf_name,
                    pdf_folder.relative_path,
                )
            except Exception as ex:
                self.ui_handler.ShowMessageError("Erron on PDF convertion")
                self.logger.error(
                    "Error creating PDF for [%s]",
                    pdf_command.pdf_name,
                )
                self.error_handler.SaveMessageError(
                    "Error on PDF conversion",
                    ex,
                )

        thread = Thread(target=process_pdf_creation)
        thread.start()
        return thread
