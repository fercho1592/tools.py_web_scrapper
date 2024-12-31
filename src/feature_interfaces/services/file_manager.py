from __future__ import annotations
from abc import ABC, abstractmethod

class IFileManager(ABC):
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
    def GetImagesInFolder(self) -> list[str]:
        pass

    @abstractmethod
    def MoveFileTo(self, fileName: str, destinyFolder: IFileManager):
        pass

    @abstractmethod
    def DeleteAll(self):
        pass
    