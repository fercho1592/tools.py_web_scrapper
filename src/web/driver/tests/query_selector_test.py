from web.driver.bs4.bs4_decoder import BeautifulSoupDecoder
from web.driver.html_parser.html_decoder import HtmlDecoder
from contracts.web_drivers.enums import CommonAttrs


def _get_bs4_dom(html: str):
    decoder = BeautifulSoupDecoder()
    decoder.set_html(html)
    return decoder.get_dom_component()


def _get_html_parser_dom(html: str):
    decoder = HtmlDecoder()
    decoder.set_html(html)
    return decoder.get_dom_component()


def _assert_selector_contract(dom):
    first_item = dom.query_selector("#root .item")
    assert first_item is not None
    assert first_item.get_attr_value(CommonAttrs.ID) == "a"

    all_items = dom.query_selector_all("#root .item")
    assert len(all_items) == 2

    href_link = dom.query_selector("a[href='/next']")
    assert href_link is not None
    assert href_link.get_value() == "Go"


def test_query_selector_with_bs4_decoder():
    html = """
    <div id='root'>
      <span id='a' class='item x'>One</span>
      <span id='b' class='item y'>Two</span>
      <a href='/next' class='btn'>Go</a>
    </div>
    """
    dom = _get_bs4_dom(html)
    _assert_selector_contract(dom)


def test_query_selector_with_html_parser_decoder():
    html = """
    <div id='root'>
      <span id='a' class='item x'>One</span>
      <span id='b' class='item y'>Two</span>
      <a href='/next' class='btn'>Go</a>
    </div>
    """
    dom = _get_html_parser_dom(html)
    _assert_selector_contract(dom)
