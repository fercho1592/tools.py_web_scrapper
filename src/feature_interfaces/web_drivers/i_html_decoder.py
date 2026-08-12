from __future__ import annotations
from abc import ABC, abstractmethod

from contracts.web_drivers.i_web_reader_driver import IWebReaderDriver


class IHtmlDecoder(ABC):
    @abstractmethod
    def set_html(self, dom_html: str) -> None:
        pass

    @abstractmethod
    def get_dom_component(self) -> IWebReaderDriver:
        pass
