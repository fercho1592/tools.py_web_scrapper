from __future__ import annotations
from abc import ABC, abstractmethod

from feature_interfaces.models.folders_struct import FolderPath


class IPdfCreator(ABC):
    @abstractmethod
    def CreatePdf(self, pdfName: str, manga_data: dict[str, str] | None):
        pass

    @abstractmethod
    def SetFileManager(self, fileManager: FolderPath):
        pass
