from __future__ import annotations
from abc import ABC, abstractmethod

from feature_interfaces.web_drivers.enums import CommonAttrs, CommonTags

class IWebElementDriver(ABC):
    @abstractmethod
    def get_value(self) -> str:
        pass
    @abstractmethod
    def get_id(self) -> str | None:
        pass
    @abstractmethod
    def add_children(self, child:IWebElementDriver):
        pass
    @abstractmethod
    def has_attr(self, attr:CommonAttrs, value: str | None = None):
        pass
    @abstractmethod
    def get_attr_value(self, attr: CommonAttrs):
        pass
    @abstractmethod
    def has(self, tag_name:CommonTags, attr: CommonAttrs | None = None, value: str | None = None):
        pass
    @abstractmethod
    def get_children_by_tag(
        self, tag_name:CommonTags, attr: CommonAttrs | None = None, value: str | None = None
    ) -> list[IWebElementDriver]:
        pass
