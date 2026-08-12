from feature.web_driver.bs4.bs4_decoder import BeautifulSoupDecoder
from feature.web_driver.html_parser.html_decoder import HtmlDecoder
from feature_interfaces.web_drivers.enums import CommonAttrs, CommonTags

HTML = """
<html>
  <body>
    <div id="main" class="content">
      <a href="https://example.com" class="link primary">Example</a>
      <span class="text">Test</span>
      <div id="nested" class="content inner">
        <a class="link">Child</a>
      </div>
    </div>
  </body>
</html>
"""


def test_bs4_decoder_query_selector():
    decoder = BeautifulSoupDecoder()
    decoder.set_html(HTML)
    root = decoder.get_dom_component()
    element = root.query_selector("#main .link.primary")
    assert element is not None
    assert element.get_attr_value(CommonAttrs.HREF) == "https://example.com"


def test_bs4_decoder_query_selector_all():
    decoder = BeautifulSoupDecoder()
    decoder.set_html(HTML)
    root = decoder.get_dom_component()
    elements = root.query_selector_all("a.link")
    assert len(elements) == 2


def test_html_decoder_query_selector():
    decoder = HtmlDecoder()
    decoder.set_html(HTML)
    root = decoder.get_dom_component()
    element = root.query_selector("#nested .link")
    assert element is not None
    assert element.get_value() == "Child"


def test_html_decoder_query_selector_all():
    decoder = HtmlDecoder()
    decoder.set_html(HTML)
    root = decoder.get_dom_component()
    elements = root.query_selector_all(".content .link")
    assert len(elements) == 2
