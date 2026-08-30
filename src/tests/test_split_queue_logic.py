from app.handlers.queue_download_handler import (
    DownloadQueueCommand,
    DownloadQueueHandler,
)
from app.handlers.split_folders_queue_handler import (
    MAX_IMAGES_PER_SPLIT_QUEUE,
    SplitFoldersQueueHandler,
)
from contracts.enums.queue_enum import QueueNameEnum


class TestSplitQueueLogic:
    def test_download_queue_routes_large_downloads_to_split_queue(self):
        command = DownloadQueueCommand(
            manga_url="https://example.com/manga",
            download_folder="/tmp/manga",
            queue_name=QueueNameEnum.DOWNLOAD.value,
            next_queue=QueueNameEnum.PDF.value,
            chapters=[("chapter_1", 1, 200)],
        )

        assert (
            DownloadQueueHandler.resolve_next_queue(command, image_count=201)
            == QueueNameEnum.SPLIT_FOLDERS.value
        )

    def test_download_queue_routes_small_downloads_to_pdf_queue(self):
        command = DownloadQueueCommand(
            manga_url="https://example.com/manga",
            download_folder="/tmp/manga",
            queue_name=QueueNameEnum.DOWNLOAD.value,
            next_queue=QueueNameEnum.PDF.value,
            chapters=[("chapter_1", 1, 120)],
        )

        assert (
            DownloadQueueHandler.resolve_next_queue(command, image_count=120)
            == QueueNameEnum.PDF.value
        )

    def test_split_queue_builds_default_chapters_for_large_download(self):
        chapters = SplitFoldersQueueHandler.build_default_chapters(
            image_count=350,
            max_images_per_split=MAX_IMAGES_PER_SPLIT_QUEUE,
        )

        assert chapters == [
            ("chapter_1", 1, 200),
            ("chapter_2", 201, 350),
        ]
