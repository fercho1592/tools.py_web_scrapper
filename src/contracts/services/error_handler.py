from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Self

class IErrorHandler(ABC):
    @abstractmethod
    def SaveDownloadError(self, message: str, item: int, totalItems:int, ex: Exception):
        pass
    @abstractmethod
    def SaveMessageError(self: Self, message: str, ex: Exception):
        pass
