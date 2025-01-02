from __future__ import annotations
from abc import ABC, abstractmethod

class IHttpService(ABC):
    @abstractmethod
    def GetHtmlFromUrl(self, web_page: str):
        pass
    @abstractmethod
    def DownloadImageFromUrl(self, url: str, imageName: str, to_folder: str):
        pass
    @abstractmethod
    def SetHeaders(self, headers: dict[str, str]):
        pass
