''' Class for html decodification '''

from html.parser import HTMLParser
from html_reader.dom_reader import HtmlElement, DomElement

class HtmlDecoder(HTMLParser):
  '''
  Implementantion to read all html string and create a list of all components
  '''

  def set_html(self, dom_html:str) -> None:
    self.components:list[HtmlElement] = []
    self.last_open:list[HtmlElement] = []
    self.feed(dom_html)

  def handle_starttag(self, tag, attrs):
    last_component = self.last_open[-1] if len(self.last_open) > 0 else None
    new_component = HtmlElement(tag, attrs, last_component)
    if last_component is not None:
      last_component.add_children(new_component)

    self.components.append(new_component)
    self.last_open.append(new_component)

  def handle_endtag(self, tag):
    del tag
    last_open = self.last_open[-1]
    self.last_open.remove(last_open)

  def handle_data(self, data):
    if len(self.last_open) == 0: return
    component = self.last_open[-1]
    component.set_value(data)

  def get_dom_component(self) -> DomElement:
    return DomElement(self.components)
