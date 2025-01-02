from html.parser import HTMLParser
from feature.html_reader.dom_reader import HtmlElement, DomElement

class HtmlDecoder(HTMLParser):
    def set_html(self, dom_html:str) -> None:
        self.Components:list[HtmlElement] = []
        self.LastOpen:list[HtmlElement] = []
        self.feed(dom_html)

    def handle_starttag(self, tag, attrs):
        last_component = self.LastOpen[-1] if len(self.LastOpen) > 0 else None
        new_component = HtmlElement(tag, attrs, last_component)
        if last_component is not None:
            last_component.add_children(new_component)

        self.Components.append(new_component)
        self.LastOpen.append(new_component)

    def handle_endtag(self, tag):
        del tag
        last_open = self.LastOpen[-1]
        self.LastOpen.remove(last_open)

    def handle_data(self, data):
        if len(self.LastOpen) == 0: return
        component = self.LastOpen[-1]
        component.set_value(data)

    def get_dom_component(self) -> DomElement:
        return DomElement(self.Components)
