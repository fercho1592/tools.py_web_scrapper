import asyncio
from dataclasses import dataclass
from threading import Thread, current_thread
import traceback
from typing import Any

from app.handlers.split_folders_queue_handler import (
    MAX_IMAGES_PER_SPLIT_QUEUE,
    SplitFoldersQueueHandler,
)
from contracts.enums.queue_enum import QueueNameEnum
from contracts.models.folders_struct import MangaFoldersStruct
from contracts.protocols.queue_handler_protocol import (
    QueueHandlerProtocol,
    QueueMessage,
)
from core.services.error_handler import ErrorLogFileHandler
from services.manga_downloader_service import MangaDownloaderCommand


@dataclass
class DownloadQueueCommand:
    manga_url: str
    download_folder: str
    queue_name: str
    next_queue: str = QueueNameEnum.PDF.value
    chapters: list[tuple[str, int, int]] | None = None


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
        manga_scrapper_factory,
    ):
        self.file_manager = file_manager
        self.logger = logger
        self.error_handler = error_handler
        self.ui_handler = ui_handler
        self.fn_manga_downloader_handler = fn_manga_downloader_handler
        self.manga_scrapper_factory = manga_scrapper_factory
        super().__init__(queue_name, next_queue)

    @staticmethod
    def resolve_next_queue(
        command: DownloadQueueCommand,
        image_count: int,
    ) -> str:
        if image_count > MAX_IMAGES_PER_SPLIT_QUEUE:
            return QueueNameEnum.SPLIT_FOLDERS.value
        return command.next_queue or QueueNameEnum.PDF.value

    def on_message(self, payload: dict[str, Any]):
        queue_message = QueueMessage[DownloadQueueCommand](**payload)

        def process_download():
            download_command = queue_message.to_command(DownloadQueueCommand)
            print(f"Processing download for {download_command.manga_url}")

            folders = MangaFoldersStruct(download_command.download_folder)
            error_handler = ErrorLogFileHandler(
                download_command.manga_url,
                folders.error_log_folder,
            )
            self.error_handler = error_handler

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
                    manga_command = MangaDownloaderCommand(
                        scrapper=self.manga_scrapper_factory(
                            download_command.manga_url
                        ),
                        pageNumber=last_page,
                        folderPath=download_folder,
                    )
                    result = self.fn_manga_downloader_handler(manga_command)
                    if asyncio.iscoroutine(result):
                        asyncio.run(result)

                image_count = len(self.file_manager.GetImagesInFolder(download_folder))
                next_queue = self.resolve_next_queue(download_command, image_count)
                if next_queue == QueueNameEnum.SPLIT_FOLDERS.value:
                    chapters = (
                        download_command.chapters
                        or SplitFoldersQueueHandler.build_default_chapters(
                            image_count,
                            max_images_per_split=MAX_IMAGES_PER_SPLIT_QUEUE,
                        )
                    )
                    download_command.chapters = chapters
                    download_command.next_queue = next_queue
                    self.ui_handler.ShowMessage(
                        "Large download detected. Routing to split folders queue."
                    )
                else:
                    download_command.next_queue = next_queue

                self.ui_handler.ShowMessage("End Manga Download")
                self.logger.info(
                    "End manga download for [%s]", download_command.manga_url
                )
            except (
                TypeError,
                ValueError,
                KeyError,
                AttributeError,
                RuntimeError,
                OSError,
            ) as ex:
                self.logger.error(
                    "Download incomplete for [%s]", download_command.manga_url
                )
                self.error_handler.SaveDownloadError("Error during manga download", ex)
                setattr(
                    current_thread(),
                    "_queue_error",
                    {
                        "error": str(ex),
                        "traceback": traceback.format_exc(),
                        "manga_url": download_command.manga_url,
                        "payload": payload,
                    },
                )

            print(f"Finished processing download for {download_command.manga_url}")

        thread = Thread(target=process_download)
        thread.start()

        return thread
