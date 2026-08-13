from __future__ import annotations

from html.parser import HTMLParser
from typing import List

from contracts.web_drivers.i_html_decoder import IHtmlDecoder
from contracts.web_drivers.i_web_reader_driver import IWebReaderDriver
from web.driver.html_parser.dom_reader import DomElement, HtmlElement


class _HtmlBuilder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack: List[HtmlElement] = []
        self.roots: List[HtmlElement] = []

    def handle_starttag(self, tag, attrs):
        attr_dict = {k: v for k, v in attrs}
        elem = HtmlElement(tag, attr_dict)
        if self.stack:
            parent = self.stack[-1]
            elem.Parent = parent
            parent.add_children(elem)
        else:
            self.roots.append(elem)
        self.stack.append(elem)

    def handle_endtag(self, tag):
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if self.stack:
            current = self.stack[-1]
            current.set_value((current.get_value() or "") + data.strip())


class HtmlDecoder(IHtmlDecoder):
    def __init__(self):
        self._dom_html = ""

    def set_html(self, dom_html: str) -> None:
        self._dom_html = dom_html

    def get_dom_component(self) -> IWebReaderDriver:
        parser = _HtmlBuilder()
        parser.feed(self._dom_html)
        return DomElement(parser.roots)
