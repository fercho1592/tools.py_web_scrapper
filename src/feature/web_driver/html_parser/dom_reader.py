from dataclasses import dataclass, field
from feature.web_driver.query_selector import query_selector, query_selector_all
from contracts.web_drivers.enums import CommonAttrs, CommonTags
from contracts.web_drivers.i_web_reader_driver import IWebReaderDriver
from contracts.web_drivers.i_web_element_driver import IWebElementDriver


@dataclass
class HtmlElement(IWebElementDriver):
    Tag: str
    Attrs: dict[str, str]
    Parent: IWebElementDriver | None = None
    Value: str | None = None
    Children: list[IWebElementDriver] = field(default_factory=list)

    def set_value(self, value: str):
        self.Value = value

    def get_value(self):
        return self.Value

    def get_id(self):
        return (
            self.Attrs[CommonAttrs.ID.value]
            if CommonAttrs.ID.value in self.Attrs
            else None
        )

    def add_children(self, child: IWebElementDriver):
        self.Children.append(child)

    def has_attr(self, attr: CommonAttrs | str, value: str | None = None) -> bool:
        key = attr.value if hasattr(attr, "value") else attr
        return key in self.Attrs and (value is None or self.Attrs[key] == value)

    def get_attr_value(self, attr: CommonAttrs | str):
        key = attr.value if hasattr(attr, "value") else attr
        return self.Attrs[key] if key in self.Attrs else None

    def has(
        self,
        tag_name: CommonTags | str,
        attr: CommonAttrs | None = None,
        value: str | None = None,
    ):
        tag = tag_name.value if hasattr(tag_name, "value") else tag_name
        if self.Tag == tag and attr is None:
            return True
        elif self.Tag == tag and (attr is not None and self.has_attr(attr, value)):
            return True
        return False

    def get_children_by_tag(
        self,
        tag_name: CommonTags,
        attr: CommonAttrs | None = None,
        value: str | None = None,
    ) -> list[IWebElementDriver]:
        result = []
        for child in self.Children:
            if child.has(tag_name, attr, value):
                result.append(child)

            result.extend(child.get_children_by_tag(tag_name, attr, value))

        return result

    def query_selector(self, selector: str) -> IWebElementDriver | None:
        return query_selector(self.Children, selector)

    def query_selector_all(self, selector: str) -> list[IWebElementDriver]:
        return query_selector_all(self.Children, selector)


class DomElement(IWebReaderDriver):
    def __init__(self, components: list[IWebElementDriver]):
        self.__components = components

    def get_by_tag_name(
        self,
        tag_name: CommonTags,
        attr: CommonAttrs | None = None,
        value: str | None = None,
    ) -> list[IWebElementDriver]:
        result: list[IWebElementDriver] = []
        for child in self.__components:
            if child.Tag == tag_name.value and attr is None:
                result.append(child)
            elif child.Tag == tag_name.value and (
                attr is not None and child.has_attr(attr, value)
            ):
                result.append(child)

            result.extend(child.get_children_by_tag(tag_name, attr, value))
        return result

    def get_by_attrs(self, attr: CommonAttrs, valule=None) -> list[IWebElementDriver]:
        result: list[IWebElementDriver] = []

        def collect(node: IWebElementDriver):
            if node.has_attr(attr, valule):
                result.append(node)
            for child in node.Children:
                collect(child)

        for comp in self.__components:
            collect(comp)

        return result

    def query_selector(self, selector: str) -> IWebElementDriver | None:
        return query_selector(self.__components, selector)

    def query_selector_all(self, selector: str) -> list[IWebElementDriver]:
        return query_selector_all(self.__components, selector)

    def get_parent(self) -> IWebElementDriver | None:
        return None
