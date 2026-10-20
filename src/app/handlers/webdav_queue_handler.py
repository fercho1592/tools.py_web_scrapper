import asyncio
import traceback
from dataclasses import dataclass
from threading import Thread, current_thread
from typing import Any

from contracts.models.folders_struct import FolderPath, MangaFoldersStruct
from contracts.protocols.queue_handler_protocol import (
    QueueHandlerProtocol,
    QueueMessage,
)
from core.services.error_handler import ErrorLogFileHandler
from services.webdav_service import WebDavCommand


@dataclass
class WebDavQueueCommand:
    manga_name: str
    pdf_path: FolderPath
    dav_path: FolderPath
    queue_name: str = ""
    next_queue: str = ""


class WebDavQueueHandler(QueueHandlerProtocol[WebDavQueueCommand]):
    def __init__(
        self,
        queue_name: str,
        next_queue: str,
        file_manager,
        logger,
        error_handler,
        ui_handler,
        fn_webdav_handler,
    ):
        self.file_manager = file_manager
        self.logger = logger
        self.error_handler = error_handler
        self.ui_handler = ui_handler
        self.fn_webdav_handler = fn_webdav_handler
        super().__init__(queue_name, next_queue)

    def build_next_queue_message(
        self,
        original_payload: dict[str, Any],
        command: WebDavQueueCommand,
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
        queue_message = QueueMessage[WebDavQueueCommand](**payload)
        webdav_command = queue_message.to_command(WebDavQueueCommand)

        def process_upload():
            folders = MangaFoldersStruct(webdav_command.manga_name)
            error_handler = ErrorLogFileHandler(
                webdav_command.manga_name,
                folders.error_log_folder,
            )
            self.error_handler = error_handler

            try:
                self.ui_handler.ShowMessage("Uploading PDF to Webdav Service")

                if not isinstance(webdav_command.pdf_path, FolderPath):
                    raise TypeError("pdf_path must be a FolderPath instance")
                if not isinstance(webdav_command.dav_path, FolderPath):
                    raise TypeError("dav_path must be a FolderPath instance")

                if self.fn_webdav_handler is not None:
                    upload_command = WebDavCommand(
                        manga_name=webdav_command.manga_name,
                        pdf_path=webdav_command.pdf_path,
                        dav_path=webdav_command.dav_path,
                    )
                    result = self.fn_webdav_handler(upload_command)
                    if asyncio.iscoroutine(result):
                        asyncio.run(result)

                next_queue_message = self.build_next_queue_message(
                    payload, webdav_command
                )
                if next_queue_message is not None:
                    setattr(current_thread(), "_next_queue_message", next_queue_message)

                self.ui_handler.ShowMessage(
                    f"PDF uploaded to WebDAV: {webdav_command.manga_name}"
                )
                self.logger.info(
                    "PDF uploaded to WebDAV for [%s]",
                    webdav_command.manga_name,
                )
            except Exception as ex:
                self.logger.error(
                    "Error uploading file to WebDAV for [%s]: %s",
                    webdav_command.manga_name,
                    ex,
                )
                self.error_handler.SaveMessageError(
                    "Error uploading file to WebDAV",
                    ex,
                )
                setattr(
                    current_thread(),
                    "_queue_error",
                    {
                        "error": str(ex),
                        "traceback": traceback.format_exc(),
                        "manga_url": webdav_command.manga_name,
                        "payload": payload,
                    },
                )

        thread = Thread(target=process_upload)
        thread.start()
        return thread
