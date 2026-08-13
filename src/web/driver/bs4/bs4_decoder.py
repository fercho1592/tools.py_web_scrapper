from __future__ import annotations

from bs4 import BeautifulSoup, Tag

from web.driver.query_selector import query_selector, query_selector_all
from contracts.web_drivers.enums import CommonAttrs, CommonTags
from contracts.web_drivers.i_html_decoder import IHtmlDecoder
from contracts.web_drivers.i_web_element_driver import IWebElementDriver
from contracts.web_drivers.i_web_reader_driver import IWebReaderDriver


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

    def query_selector(self, selector: str) -> IWebElementDriver | None:
        return query_selector(self.Children, selector)

    def query_selector_all(self, selector: str) -> list[IWebElementDriver]:
        return query_selector_all(self.Children, selector)


class SoupDomElement(IWebReaderDriver):
    def __init__(self, components: list[IWebElementDriver]):
        self.Components = components

    def get_by_tag_name(
        self,
        tag_name: CommonTags,
        attr: CommonAttrs | None = None,
        value: str | None = None,
    ) -> list[IWebElementDriver]:
        result: list[IWebElementDriver] = []
        for node in self.Components:
            if node.has(tag_name, attr, value):
                result.append(node)
            result.extend(node.get_children_by_tag(tag_name, attr, value))
        return result

    def get_by_attrs(
        self, attr: CommonAttrs, valule: str | None = None
    ) -> list[IWebElementDriver]:
        result: list[IWebElementDriver] = []

        def collect(node: IWebElementDriver):
            if node.has_attr(attr, valule):
                result.append(node)
            for child in node.Children:
                collect(child)

        for root in self.Components:
            collect(root)
        return result

    def query_selector(self, selector: str) -> IWebElementDriver | None:
        return query_selector(self.Components, selector)

    def query_selector_all(self, selector: str) -> list[IWebElementDriver]:
        return query_selector_all(self.Components, selector)

    def get_parent(self) -> IWebElementDriver | None:
        return None


class BeautifulSoupDecoder(IHtmlDecoder):
    def __init__(self):
        self._dom_html = ""

    def set_html(self, dom_html: str) -> None:
        self._dom_html = dom_html

    def get_dom_component(self) -> IWebReaderDriver:
        soup = BeautifulSoup(self._dom_html, "html.parser")
        roots = [
            SoupElement(node)
            for node in soup.find_all(recursive=False)
            if isinstance(node, Tag)
        ]
        return SoupDomElement(roots)
