import asyncio
from dataclasses import dataclass
from threading import Thread

from contracts.models.folders_struct import MangaFoldersStruct
from contracts.protocols.queue_handler_protocol import (
    QueueHandlerProtocol,
    QueueMessage,
)


@dataclass
class DownloadQueueCommand:
    manga_url: str
    download_folder: str
    queue_name: str
    next_queue: str


class DownloadQueueHandler(QueueHandlerProtocol[DownloadQueueCommand]):
    def __init__(
        self,
        queue_name: str,
        next_queue: str,
        file_manager,
        logger,
        error_handler,
        ui_handler,
        fn_manga_downloader_handler,
    ):
        self.file_manager = file_manager
        self.logger = logger
        self.error_handler = error_handler
        self.ui_handler = ui_handler
        self.fn_manga_downloader_handler = fn_manga_downloader_handler
        super().__init__(queue_name, next_queue)

    def on_message(self, command: QueueMessage[DownloadQueueCommand]):
        def process_download():
            download_command = command.messageCommand
            print(f"Processing download for {download_command.manga_url}")
            try:
                download_folder = download_command.download_folder
                if isinstance(download_folder, str):
                    download_folder = MangaFoldersStruct(
                        download_folder
                    ).download_folder

                last_page = self.file_manager.get_last_downloaded_page(download_folder)
                self.ui_handler.ShowMessage(
                    f"Start download of {download_command.manga_url} in [{download_folder}] from page [{last_page}]"
                )

                if self.fn_manga_downloader_handler is not None:
                    result = self.fn_manga_downloader_handler(download_command)
                    if asyncio.iscoroutine(result):
                        asyncio.run(result)

                self.ui_handler.ShowMessage("End Manga Download")
                self.logger.info(
                    "End manga download for [%s]", download_command.manga_url
                )
            except Exception as ex:
                self.logger.error(
                    "Download incomplete for [%s]", download_command.manga_url
                )
                self.error_handler.SaveDownloadError("Error during manga download", ex)

            print(f"Finished processing download for {download_command.manga_url}")

        thread = Thread(target=process_download)
        thread.start()
        
        return thread
