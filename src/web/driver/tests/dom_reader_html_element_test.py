from web.driver.html_parser.dom_reader import HtmlElement, DomElement
from contracts.web_drivers.enums import CommonAttrs, CommonTags


def test_html_element_accepts_enum_and_str_attr_access():
    node = HtmlElement("div", {"id": "root", "class": "a b"})

    assert node.has_attr(CommonAttrs.ID, "root")
    assert node.has_attr("class")
    assert node.get_attr_value(CommonAttrs.CLASS) == "a b"
    assert node.get_attr_value("id") == "root"


def test_dom_element_get_by_attrs_is_recursive():
    root = HtmlElement("div", {"id": "root"})
    child = HtmlElement("a", {"href": "/manga/1"}, Parent=root)
    root.add_children(child)

    dom = DomElement([root])
    href_nodes = dom.get_by_attrs(CommonAttrs.HREF)

    assert len(href_nodes) == 1
    assert href_nodes[0].get_attr_value(CommonAttrs.HREF) == "/manga/1"


def test_dom_element_get_by_tag_name_recursive():
    root = HtmlElement("div", {})
    parent = HtmlElement("ul", {}, Parent=root)
    root.add_children(parent)
    child = HtmlElement("li", {}, Parent=parent)
    parent.add_children(child)

    dom = DomElement([root])
    li_nodes = dom.get_by_tag_name(CommonTags.LI)

    assert len(li_nodes) == 1
