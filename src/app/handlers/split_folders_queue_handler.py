import os
from dataclasses import dataclass
from threading import Thread

from contracts.enums.queue_enum import QueueNameEnum
from contracts.models.folders_struct import MangaFoldersStruct
from contracts.protocols.queue_handler_protocol import (
    QueueHandlerProtocol,
    QueueMessage,
)

MAX_IMAGES_PER_SPLIT_QUEUE = 200


@dataclass
class SplitFoldersQueueCommand:
    manga_url: str
    download_folder: str
    chapters: list[tuple[str, int, int]] | None = None
    queue_name: str = QueueNameEnum.SPLIT_FOLDERS.value
    next_queue: str = QueueNameEnum.PDF.value


class SplitFoldersQueueHandler(QueueHandlerProtocol[SplitFoldersQueueCommand]):
    def __init__(
        self,
        queue_name: str,
        next_queue: str,
        file_manager,
        logger,
        error_handler,
        ui_handler,
    ):
        self.file_manager = file_manager
        self.logger = logger
        self.error_handler = error_handler
        self.ui_handler = ui_handler
        super().__init__(queue_name, next_queue)

    @staticmethod
    def build_default_chapters(
        image_count: int,
        max_images_per_split: int = MAX_IMAGES_PER_SPLIT_QUEUE,
    ) -> list[tuple[str, int, int]]:
        if image_count <= 0:
            return []

        chapters: list[tuple[str, int, int]] = []
        chapter_number = 1
        start = 1

        while start <= image_count:
            end = min(start + max_images_per_split - 1, image_count)
            chapters.append((f"chapter_{chapter_number}", start, end))
            chapter_number += 1
            start = end + 1

        return chapters

    def on_message(self, payload: dict):
        queue_message = QueueMessage[SplitFoldersQueueCommand](**payload)
        split_command = queue_message.to_command(SplitFoldersQueueCommand)

        def process_split():
            folder_structure = MangaFoldersStruct(split_command.download_folder)
            base_folder = folder_structure.download_folder

            try:
                images = self.file_manager.GetImagesInFolder(base_folder)
                if not images:
                    self.logger.info(
                        "No images found to split for [%s]",
                        split_command.manga_url,
                    )
                    return

                chapters = split_command.chapters or self.build_default_chapters(
                    len(images),
                    MAX_IMAGES_PER_SPLIT_QUEUE,
                )
                if not chapters:
                    return

                for chapter_name, start_page, end_page in chapters:
                    subfolder_path = os.path.join(base_folder.full_path, chapter_name)
                    os.makedirs(subfolder_path, exist_ok=True)

                    selected_images = images[start_page - 1 : end_page]
                    for image_name in selected_images:
                        source_path = os.path.join(base_folder.full_path, image_name)
                        target_path = os.path.join(subfolder_path, image_name)
                        if os.path.exists(target_path):
                            continue
                        os.replace(source_path, target_path)

                self.ui_handler.ShowMessage(
                    f"Split folders created for [{split_command.manga_url}]"
                )
                self.logger.info(
                    "Split folders created for [%s] with %s chapters",
                    split_command.manga_url,
                    len(chapters),
                )
            except Exception as exc:  # pragma: no cover - queue execution guard
                self.logger.error(
                    "Error creating split folders for [%s]",
                    split_command.manga_url,
                )
                if self.error_handler is not None:
                    self.error_handler.SaveMessageError(
                        "Error creating split folders",
                        exc,
                    )

        thread = Thread(target=process_split)
        thread.start()
        return thread
