from __future__ import annotations
from abc import ABC, abstractmethod

from feature_interfaces.web_drivers.enums import CommonAttrs, CommonTags

class IWebElementDriver(ABC):
    @abstractmethod
    def get_value(self):
        pass
    @abstractmethod
    def get_id(self):
        pass
    @abstractmethod
    def add_children(self, child:IWebElementDriver):
        pass
    @abstractmethod
    def has_attr(self, attr:str, value: str = None):
        pass
    @abstractmethod
    def get_attr_value(self, attr: str):
        pass
    @abstractmethod
    def get_children_by_tag(
        self, tag_name:CommonTags, attr: CommonAttrs = None, value: str = None
    ) -> list[IWebElementDriver]:
        pass
