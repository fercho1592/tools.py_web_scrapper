import asyncio
from dataclasses import dataclass
from threading import Thread

from contracts.models.folders_struct import FolderPath
from contracts.protocols.queue_handler_protocol import (
    QueueHandlerProtocol,
    QueueMessage,
)


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

    def on_message(self, command: QueueMessage[WebDavQueueCommand]):
        def process_upload():
            webdav_command = command.messageCommand
            try:
                self.ui_handler.ShowMessage("Uploading PDF to Webdav Service")

                if not isinstance(webdav_command.pdf_path, FolderPath):
                    raise TypeError("pdf_path must be a FolderPath instance")
                if not isinstance(webdav_command.dav_path, FolderPath):
                    raise TypeError("dav_path must be a FolderPath instance")

                if self.fn_webdav_handler is not None:
                    result = self.fn_webdav_handler(webdav_command)
                    if asyncio.iscoroutine(result):
                        asyncio.run(result)

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

        thread = Thread(target=process_upload)
        thread.start()
        return thread
