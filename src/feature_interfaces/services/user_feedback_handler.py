from __future__ import annotations
from abc import ABC, abstractmethod

class IUserFeedbackHandler(ABC):
    @abstractmethod
    def ShowMessage(self, message: str):
        pass
    @abstractmethod
    def ShowMessageError(self, message: str, ex: Exception):
        pass
    @abstractmethod
    def CreateProgressBar(self, itemsNumber: int, descriptionMessage: str) -> IProgressBar:
        pass

class IProgressBar(ABC):
    @abstractmethod
    def SetCurrentProcess(self,currentItemNumber:int) -> None:
        pass
    @abstractmethod
    def NextItem(self) -> None:
        pass
