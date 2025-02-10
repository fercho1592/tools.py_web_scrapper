from __future__ import annotations
from abc import ABC, abstractmethod
from feature_interfaces.services.file_manager import IFileScrapperManager

class IPdfCreator(ABC):
    @abstractmethod
    def CreatePdf(self, pdfName: str, manga_data: dict[str,str] | None):
        pass

    @abstractmethod
    def SetFileManager(self, fileManager: IFileScrapperManager):
        pass
