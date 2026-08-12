from __future__ import annotations

from bs4 import BeautifulSoup, Tag

from feature_interfaces.web_drivers.enums import CommonAttrs, CommonTags
from feature_interfaces.web_drivers.i_web_element_driver import IWebElementDriver
from feature_interfaces.web_drivers.i_web_reader_driver import IWebReaderDriver


def _normalize_attr_value(value: str | list[str] | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        return " ".join(str(item) for item in value)
    return str(value)


class SoupElement(IWebElementDriver):
    def __init__(self, tag: Tag, parent: IWebElementDriver | None = None):
        self.Tag: str = tag.name
        self.Attrs: dict[str, str] = {
            key: _normalize_attr_value(value)
            for key, value in tag.attrs.items()
            if _normalize_attr_value(value) is not None
        }
        self.Parent: IWebElementDriver | None = parent
        self.Value: str = tag.get_text(strip=True)
        self.Children: list[IWebElementDriver] = [
            SoupElement(child, self)
            for child in tag.find_all(recursive=False)
            if isinstance(child, Tag)
        ]

    def get_value(self) -> str:
        return self.Value

    def get_id(self) -> str | None:
        return self.Attrs.get(CommonAttrs.ID.value)

    def add_children(self, child: IWebElementDriver):
        child.Parent = self
        self.Children.append(child)

    def has_attr(self, attr: CommonAttrs, value: str | None = None) -> bool:
        if attr.value not in self.Attrs:
            return False
        if value is None:
            return True
        return self.Attrs[attr.value] == value

    def get_attr_value(self, attr: CommonAttrs):
        return self.Attrs.get(attr.value)

    def has(
        self,
        tag_name: CommonTags,
        attr: CommonAttrs | None = None,
        value: str | None = None,
    ) -> bool:
        if self.Tag != tag_name.value:
            return False
        if attr is None:
            return True
        return self.has_attr(attr, value)

    def get_children_by_tag(
        self,
        tag_name: CommonTags,
        attr: CommonAttrs | None = None,
        value: str | None = None,
    ) -> list[IWebElementDriver]:
        result: list[IWebElementDriver] = []
        for child in self.Children:
            if child.has(tag_name, attr, value):
                result.append(child)
            result.extend(child.get_children_by_tag(tag_name, attr, value))
        return result


class SoupDomElement(IWebReaderDriver):
    def __init__(self, components: list[IWebElementDriver]):
        self.__components = components

    def get_by_tag_name(
        self,
        tag_name: CommonTags,
        attr: CommonAttrs | None = None,
        value: str | None = None,
    ) -> list[IWebElementDriver]:
        result: list[IWebElementDriver] = []
        for component in self.__components:
            if component.has(tag_name, attr, value):
                result.append(component)
            result.extend(component.get_children_by_tag(tag_name, attr, value))

        return result

    def get_by_attrs(
        self, attr: CommonAttrs, valule: str | None = None
    ) -> list[IWebElementDriver]:
        return [
            component
            for component in self.__components
            if component.has_attr(attr, valule)
        ]

    def get_parent(self) -> IWebElementDriver | None:
        return None


class BeautifulSoupDecoder:
    def __init__(self):
        self.Components: list[IWebElementDriver] = []

    def set_html(self, dom_html: str) -> None:
        soup = BeautifulSoup(dom_html, "html.parser")
        self.Components = [
            SoupElement(tag)
            for tag in soup.find_all(recursive=False)
            if isinstance(tag, Tag)
        ]

    def get_dom_component(self) -> IWebReaderDriver:
        return SoupDomElement(self.Components)
