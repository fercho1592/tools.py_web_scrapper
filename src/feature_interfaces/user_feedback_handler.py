from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Self

class IUserFeedbackHandler(ABC):
    @abstractmethod
    def SetCurrentProcess(self:Self,currentItemNumber:int) -> None:
        pass
    @abstractmethod
    def ShowMessage(self: Self, message: str):
        pass
    @abstractmethod
    def ShowErrorMessage(self: Self, message: str) -> None:
        pass
    @abstractmethod
    def NextItem(self: Self) -> None:
        pass
