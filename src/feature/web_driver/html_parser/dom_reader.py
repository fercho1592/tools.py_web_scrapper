from feature_interfaces.web_drivers.enums import CommonAttrs, CommonTags
from typing import Self
from feature_interfaces.web_drivers.i_web_reader_driver import IWebReaderDriver
from feature_interfaces.web_drivers.i_web_element_driver import IWebElementDriver

class HtmlElement(IWebElementDriver):
    def __init__(
        self, tag:str, attrs:list[tuple[str, str | None]], parent:Self = None):
        self.Tag = tag
        self.Attrs = attrs
        self.Parent = parent
        self.Children:list[Self] = []
        self.Value = None

    def set_value(self, value:str):
        self.Value = value

    def get_value(self):
        return self.Value

    def get_id(self):
        id_attr = [attr for attr in self.Attrs if attr[0] == CommonAttrs.ID.value]
        return id_attr[0][1] if len(id_attr) > 0 else None

    def add_children(self, child:Self):
        self.Children.append(child)

    def has_attr(self, attr:CommonAttrs, value: str = None):
        for atribute in self.Attrs:
            if atribute[0] != attr.value:
                continue
            if value is not None and atribute[1] != value:
                continue
            return True
        return False

    def get_attr_value(self, attr: CommonAttrs):
        for atribute in self.Attrs:
            if atribute[0] != attr.value:
                continue

            return atribute[1]
        return None

    def get_children_by_tag(
        self, tag_name:CommonTags, attr: CommonAttrs = None, value: str = None
    ) -> list[Self]:
        result = []
        for child in self.Children:
            if(child.Tag == tag_name.value and attr is None):
                result.append(child)
            elif (child.Tag == tag_name.value\
                   and (attr is not None and child.has_attr(attr, value))):
                result.append(child)

            result.extend(child.get_children_by_tag(tag_name, attr, value))

        return result

class DomElement(IWebReaderDriver):
    def __init__(self, components:list[HtmlElement]):
        self.__components = components

    def get_by_tag_name(
        self, 
        tag_name: CommonTags,
        attr: CommonAttrs = None,
        value: str = None
    ) -> list[IWebElementDriver]:
        result = []
        for child in self.__components:
            if(child.Tag == tag_name.value and attr is None):
                result.append(child)
            elif (child.Tag == tag_name.value\
                   and (attr is not None and child.has_attr(attr.value, value))):
                result.append(child)

            result.extend(child.get_children_by_tag(tag_name, attr, value))

        return result

    def get_by_attrs(self, attr: CommonAttrs, valule = None) -> list[IWebElementDriver]:
        return [comp for comp in self.__components if comp.has_attr(attr, valule)]
