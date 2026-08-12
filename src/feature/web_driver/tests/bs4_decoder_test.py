from feature.web_driver.bs4.bs4_decoder import BeautifulSoupDecoder
from feature_interfaces.web_drivers.enums import CommonAttrs, CommonTags

HTML = """
<html>
  <body>
    <div id=\"main\" class=\"content\">
      <a href=\"https://example.com\">Example</a>
      <img src=\"/image.png\" title=\"cover\" />
    </div>
  </body>
</html>
"""


def test_bs4_decoder_get_by_tag():
    decoder = BeautifulSoupDecoder()
    decoder.set_html(HTML)
    links = decoder.get_dom_component().get_by_tag_name(CommonTags.ANCHOR)
    assert len(links) == 1
    assert links[0].get_value() == "Example"
    assert links[0].get_attr_value(CommonAttrs.HREF) == "https://example.com"


def test_bs4_decoder_get_by_attrs():
    decoder = BeautifulSoupDecoder()
    decoder.set_html(HTML)
    divs = decoder.get_dom_component().get_by_attrs(CommonAttrs.ID, "main")
    assert len(divs) == 1
    assert divs[0].get_attr_value(CommonAttrs.CLASS) == "content"


def test_bs4_decoder_children_and_parent():
    decoder = BeautifulSoupDecoder()
    decoder.set_html(HTML)
    divs = decoder.get_dom_component().get_by_tag_name(CommonTags.DIV)
    assert len(divs) == 1
    imgs = divs[0].get_children_by_tag(CommonTags.IMG)
    assert len(imgs) == 1
    assert imgs[0].get_attr_value(CommonAttrs.TITLE) == "cover"
    assert imgs[0].Parent is not None
    assert imgs[0].Parent.get_attr_value(CommonAttrs.ID) == "main"
