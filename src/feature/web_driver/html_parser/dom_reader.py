from dataclasses import dataclass
from feature_interfaces.web_drivers.enums import CommonAttrs, CommonTags
from feature_interfaces.web_drivers.i_web_reader_driver import IWebReaderDriver
from feature_interfaces.web_drivers.i_web_element_driver import IWebElementDriver

@dataclass
class HtmlElement(IWebElementDriver):
    Tag:str
    Attrs: dict[str, str]
    Parent: IWebElementDriver | None = None
    Value: str | None = None
    Children:list[IWebElementDriver] = []

    def set_value(self, value:str):
        self.Value = value

    def get_value(self):
        return self.Value

    def get_id(self):
        return self.Attrs[CommonAttrs.ID.value] if CommonAttrs.ID.value in self.Attrs else None

    def add_children(self, child: IWebElementDriver):
        self.Children.append(child)

    def has_attr(self, attr:CommonAttrs, value: str | None = None) -> bool:
        return attr.value in self.Attrs and (value is None or self.Attrs[attr.value] == value)

    def get_attr_value(self, attr: CommonAttrs):
        return self.Attrs[attr.value] if attr.value in self.Attrs else None

    def has(self, tag_name:CommonTags, attr: CommonAttrs | None = None, value: str | None = None):
        if(self.Tag == tag_name.value and attr is None):
            return True
        elif (self.Tag == tag_name.value\
                and (attr is not None and self.has_attr(attr, value))):
            return True
        return False

    def get_children_by_tag(
        self, tag_name:CommonTags, attr: CommonAttrs | None = None, value: str | None = None
    ) -> list[IWebElementDriver]:
        result = []
        for child in self.Children:
            if child.has(tag_name, attr, value):
                result.append(child)

            result.extend(child.get_children_by_tag(tag_name, attr, value))

        return result

class DomElement(IWebReaderDriver):
    def __init__(self, components:list[IWebElementDriver]):
        self.__components = components

    def get_by_tag_name(
        self,
        tag_name: CommonTags,
        attr: CommonAttrs | None = None,
        value: str | None = None
    ) -> list[IWebElementDriver]:
        result: list[IWebElementDriver] = []
        for child in self.__components:
            if(child.Tag == tag_name.value and attr is None):
                result.append(child)
            elif (child.Tag == tag_name.value\
                   and (attr is not None and child.has_attr(attr, value))):
                result.append(child)

            result.extend(child.get_children_by_tag(tag_name, attr, value))
        return result

    def get_by_attrs(self, attr: CommonAttrs, valule = None) -> list[IWebElementDriver]:
        return [comp for comp in self.__components if comp.has_attr(attr, valule)]
