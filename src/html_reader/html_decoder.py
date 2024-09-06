''' Class for html decodification '''

from html.parser import HTMLParser
from .dom_reader import HtmlComponent, DomComponent

class HtmlDecoder(HTMLParser):
  '''
  Implementantion to read all html string and create a list of all components
  '''

  def set_html(self, dom_html):
    self.components = []
    self.last_open = []
    self.feed(dom_html)

  def handle_starttag(self, tag, attrs):
    last_component = self.lastOpen[-1] if len(self.lastOpen) > 0 else None
    new_component = HtmlComponent(tag, attrs, last_component)
    if last_component is not None:
      last_component.AddChildren(new_component)

    self.components.append(new_component)
    self.last_open.append(new_component)

  def handle_endtag(self, tag):
    del tag
    last_open = self.lastOpen[-1]
    self.last_open.remove(last_open)

  def handle_data(self, data):
    if len(self.lastOpen) == 0: return
    component = self.lastOpen[-1]
    component.SetValue(data)

  def get_dom_component(self):
    return DomComponent(self.components)
