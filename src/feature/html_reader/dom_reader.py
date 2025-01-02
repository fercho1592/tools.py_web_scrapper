'''Structure to read, move and get information about HTML'''

import feature.html_reader.common_attrs as CommonAttr
from typing import Self

class HtmlElement:
    '''
    Structure for any Html Element
    '''
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
        id_attr = [attr for attr in self.Attrs if attr[0] == CommonAttr.ID]
        return id_attr[0][1] if len(id_attr) > 0 else None

    def add_children(self, child:Self):
        self.Children.append(child)

    def has_attr(self, attr:str, value: str = None):
        for atribute in self.Attrs:
            if atribute[0] != attr:
                continue
            if value is not None and atribute[1] != value:
                continue
            return True
        return False

    def get_attr_value(self, attr: str):
        for atribute in self.Attrs:
            if atribute[0] != attr:
                continue

            return atribute[1]
        return None

    def get_children_by_tag(
        self, tag_name:str, attr: str = None, value: str = None
    ) -> list[Self]:
        result = []
        for child in self.Children:
            if(child.Tag == tag_name and attr is None):
                result.append(child)
            elif (child.Tag == tag_name\
                   and (attr is not None and child.has_attr(attr, value))):
                result.append(child)

            result.extend(child.get_children_by_tag(tag_name, attr, value))

        return result

class DomElement:
    '''
    Structure for Dom element
    '''

    def __init__(self, components:list[HtmlElement]):
        self.__components = components

    def get_by_tag_name(
        self, tag_name:str,
        attr: str = None,
        value: str = None
    ) -> list[HtmlElement]:
        result = []
        for child in self.__components:
            if(child.Tag == tag_name and attr is None):
                result.append(child)
            elif (child.Tag == tag_name\
                   and (attr is not None and child.has_attr(attr, value))):
                result.append(child)

            result.extend(child.get_children_by_tag(tag_name, attr, value))

        return result

    def get_by_attrs(self, attr, valule = None) -> list[HtmlElement]:
        return [comp for comp in self.__components if comp.has_attr(attr, valule)]
