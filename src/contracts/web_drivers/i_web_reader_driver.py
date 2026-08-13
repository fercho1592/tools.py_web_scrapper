from __future__ import annotations
from abc import ABC, abstractmethod
from contracts.web_drivers.enums import CommonAttrs, CommonTags
from contracts.web_drivers.i_web_element_driver import IWebElementDriver


class IWebReaderDriver(ABC):
    @abstractmethod
    def get_by_tag_name(
        self,
        tag_name: CommonTags,
        attr: CommonAttrs | None = None,
        value: str | None = None,
    ) -> list[IWebElementDriver]:
        pass

    @abstractmethod
    def get_by_attrs(
        self, attr: CommonAttrs, valule: str | None = None
    ) -> list[IWebElementDriver]:
        pass

    @abstractmethod
    def query_selector(self, selector: str) -> IWebElementDriver | None:
        pass

    @abstractmethod
    def query_selector_all(self, selector: str) -> list[IWebElementDriver]:
        pass

    @abstractmethod
    def get_parent(self) -> IWebElementDriver | None:
        pass
