from __future__ import annotations
from abc import ABC, abstractmethod

class IFileScrapperManager(ABC):
    @abstractmethod
    def GetFolderPath(self):
        pass

    @abstractmethod
    def GetRootPath(self):
        pass

    @abstractmethod
    def HasFile(self, fileName: str) -> bool:
        pass

    @abstractmethod
    def GetFilePath(self, fileName: str) -> str:
        pass

    @abstractmethod
    def GetImagesInFolder(self) -> list[str]:
        pass

    @abstractmethod
    def MoveFileTo(self, fileName: str, destinyFolder: IFileScrapperManager):
        pass

    @abstractmethod
    def DeleteAll(self, fromRootFolder: bool):
        pass

    @abstractmethod
    def DeleteFile(self, file: str):
        pass
