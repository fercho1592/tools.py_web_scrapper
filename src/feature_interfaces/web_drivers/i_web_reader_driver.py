from __future__ import annotations
from abc import ABC, abstractmethod
from feature_interfaces.web_drivers.i_web_element_driver import IWebElementDriver

class IWebReaderDriver(ABC):
    @abstractmethod
    def get_by_tag_name(
        self, tag_name:str,
        attr: str = None,
        value: str = None
    ) -> list[IWebElementDriver]:
        pass

    @abstractmethod
    def get_by_attrs(self, attr, valule = None) -> list[IWebElementDriver]:
        pass
