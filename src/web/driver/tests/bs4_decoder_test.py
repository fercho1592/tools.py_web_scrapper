from web.driver.bs4.bs4_decoder import BeautifulSoupDecoder
from contracts.web_drivers.enums import CommonAttrs, CommonTags


def test_bs4_decoder_get_by_attrs_is_recursive():
    html = """
    <div id='root'>
      <div class='group'>
        <a href='/manga/1' class='target'>Chapter 1</a>
      </div>
    </div>
    """
    decoder = BeautifulSoupDecoder()
    decoder.set_html(html)
    dom = decoder.get_dom_component()

    anchors = dom.get_by_attrs(CommonAttrs.HREF)
    assert len(anchors) == 1
    assert anchors[0].get_attr_value(CommonAttrs.HREF) == "/manga/1"


def test_bs4_decoder_get_by_tag_name_is_recursive():
    html = """
    <section>
      <ul>
        <li><a href='/x'>X</a></li>
        <li><a href='/y'>Y</a></li>
      </ul>
    </section>
    """
    decoder = BeautifulSoupDecoder()
    decoder.set_html(html)
    dom = decoder.get_dom_component()

    links = dom.get_by_tag_name(CommonTags.ANCHOR)
    assert len(links) == 2
    assert [item.get_value() for item in links] == ["X", "Y"]
