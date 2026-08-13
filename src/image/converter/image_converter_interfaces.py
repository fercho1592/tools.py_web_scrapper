from __future__ import annotations

from contracts.models.folders_struct import FolderPath
from typing import Protocol


class IImageEditorService(Protocol):
    def convert_image(
        self,
        folder_manager: FolderPath,
        image_name: str,
        new_image_name: str,
        destinyFolder: FolderPath,
    ): ...

    def get_image_size(self, folder_manager: FolderPath, image_name: str): ...
