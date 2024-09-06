'''Structure to read, move and get information about HTML'''

from enums.common_tags import CommonAttr
from typing import Self

class HtmlElement:
  '''
  Structure for any Html Element
  '''
  def __init__(self, tag:str, attrs:list[tuple[str, str | None]], parent:Self = None):
    self.tag = tag
    self.attrs = attrs
    self.parent = parent
    self.children = []
    self.value = None

  def set_value(self, value:str):
    self.value = value

  def get_value(self):
    return self.value

  def get_id(self):
    id_attr = [attr for attr in self.attrs if attr[0] == CommonAttr.ID]
    return id_attr[0][1] if len(id_attr) > 0 else None

  def add_children(self, child:Self):
    self.children.append(child)

  def has_attr(self, attr:str, value: str = None):
    for atribute in self.attrs:
      if atribute[0] != attr:
        continue
      if value is not None and atribute[1] != value:
        continue

      return True
    return False

  def get_attr_value(self, attr: str):
    for atribute in self.attrs:
      if atribute[0] != attr:
        continue

      return atribute[1]
    return None

  def get_children_by_tag(
      self, tag_name:str, attr: str = None, value: str = None) -> list[Self]:
    result = []
    for child in self.children:
      if(child.tag == tag_name and attr is None):
        result.append(child)
      elif (child.tag == tag_name and
            (attr is not None and child.HasAttr(attr, value))):
        result.append(child)

      result.extend(child.GetChildrenByTag(tag_name, attr, value))

    return result

class DomElement:
  '''
  Structure for Dom element
  '''

  def __init__(self, components):
    self.__components = components

  def get_by_tag_name(self, tag_name:str) -> list[HtmlElement]:
    return [comp for comp in self.__components if tag_name == comp.tag]

  def get_by_attrs(self, attr, valule = None) -> list[HtmlElement]:
    return [comp for comp in self.__components if comp.HasAttr(attr, valule)]
