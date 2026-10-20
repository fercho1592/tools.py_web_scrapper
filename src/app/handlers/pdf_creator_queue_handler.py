import asyncio
import traceback
from dataclasses import dataclass
from threading import Thread, current_thread
from typing import Any

from contracts.enums.queue_enum import QueueNameEnum
from contracts.models.folders_struct import FolderPath, MangaFoldersStruct
from contracts.protocols.queue_handler_protocol import (
    QueueHandlerProtocol,
    QueueMessage,
)
from core.services.error_handler import ErrorLogFileHandler
from services.pdf_creator_service import PDFCreatorCommand


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

    def build_next_queue_message(
        self,
        original_payload: dict[str, Any],
        command: PDFCreateQueueCommand,
    ) -> dict[str, Any] | None:
        if not command.next_queue:
            return None

        original_message = (
            original_payload.get("messageCommand", {})
            if isinstance(original_payload, dict)
            else {}
        )
        if not isinstance(original_message, dict):
            original_message = {}

        next_message = {
            **original_message,
            "queue_name": command.next_queue,
            "next_queue": command.next_queue,
        }

        return {
            "id": original_payload.get("id", ""),
            "queue_name": command.next_queue,
            "messageCommand": next_message,
            "errorLog": list(original_payload.get("errorLog", [])),
        }

    def on_message(self, payload: dict):
        queue_message = QueueMessage[PDFCreateQueueCommand](**payload)
        pdf_command = queue_message.to_command(PDFCreateQueueCommand)

        def process_pdf_creation():
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
                creator_command = PDFCreatorCommand(
                    image_folder=pdf_command.image_folder,
                    pdf_folder=pdf_command.pdf_folder,
                    pdf_name=pdf_command.pdf_name,
                    manga_data=pdf_command.manga_data,
                )
                result = self.fn_pdf_creator_handler(creator_command)
                if asyncio.iscoroutine(result):
                    asyncio.run(result)

                pdf_command.next_queue = QueueNameEnum.WEBDAV.value
                next_queue_message = self.build_next_queue_message(payload, pdf_command)
                if next_queue_message is not None:
                    setattr(current_thread(), "_next_queue_message", next_queue_message)

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
                setattr(
                    current_thread(),
                    "_queue_error",
                    {
                        "error": str(ex),
                        "traceback": traceback.format_exc(),
                        "manga_url": pdf_command.pdf_name,
                        "payload": payload,
                    },
                )

        thread = Thread(target=process_pdf_creation)
        thread.start()
        return thread
