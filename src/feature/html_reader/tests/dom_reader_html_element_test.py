#import pytest
from ..dom_reader import HtmlElement
from ..enums import CommonAttrs, CommonTags

ID_VALUE = "id-element"
CLASS_VALUE = "class-value"

class Test:
    EMPTY_ELEMENT = HtmlElement(CommonTags.ANCHOR.value, [])
    DEFAULT_ELEMENT = HtmlElement(CommonTags.ANCHOR.value, [
        (CommonAttrs.ID.value, ID_VALUE),
        (CommonAttrs.CLASS.value, CLASS_VALUE)
    ])
    CHILDREN_ELEMENTS = [
        HtmlElement(CommonTags.IMG.value, [(CommonAttrs.ID.value, ID_VALUE),]),
        HtmlElement(CommonTags.ANCHOR.value, []),
        HtmlElement(CommonTags.I.value, []),
        HtmlElement(CommonTags.H1.value, []),
        HtmlElement(CommonTags.H3.value, []),
    ]

    def test_get_id_has_no_id_returns_none(self):
        assert Test.EMPTY_ELEMENT.get_id() is None

    def test_get_id_has_id_returns_id(self):
        assert Test.DEFAULT_ELEMENT.get_id() == ID_VALUE

    def test_has_attr_has_attr_return_true(self):
        assert Test.DEFAULT_ELEMENT.has_attr(CommonAttrs.CLASS.value)

    def test_has_attr_no_has_attr_return_false(self):
        assert Test.EMPTY_ELEMENT.has_attr(CommonAttrs.CLASS.value) is False

    def test_get_attr_value_no_has_attr_return_none(self):
        assert Test.EMPTY_ELEMENT.get_attr_value(CommonAttrs.CLASS.value) is None

    def test_get_attr_value_has_attr_return_value(self):
        assert Test.DEFAULT_ELEMENT.get_attr_value(CommonAttrs.CLASS.value) == CLASS_VALUE

    def test_get_childen_by_tag_has_childen_return_child(self):
        obj = HtmlElement(CommonTags.SPAN.value, [])
        for ele in Test.CHILDREN_ELEMENTS:
            obj.add_children(ele)

        ele_obtained = obj.get_children_by_tag(CommonTags.H3.value)
        assert ele_obtained is not None
        assert len(ele_obtained) == 1

    def test_get_childen_by_tag_has_nessted_childen_return_child(self):
        obj = HtmlElement(CommonTags.SPAN.value, [])
        child = HtmlElement(CommonTags.SPAN.value, [])
        for ele in Test.CHILDREN_ELEMENTS:
            child.add_children(ele)
        obj.add_children(child)
        ele_obtained = obj.get_children_by_tag(CommonTags.H3.value)
        assert ele_obtained is not None
        assert len(ele_obtained) == 1

    def test_get_childen_by_tag_has_no_childen_return_none(self):
        obj = HtmlElement(CommonTags.SPAN.value, [])
        child = HtmlElement(CommonTags.SPAN.value, [])
        for ele in Test.CHILDREN_ELEMENTS:
            child.add_children(ele)
        obj.add_children(child)
        ele_obtained = obj.get_children_by_tag(CommonTags.OPTION.value)
        assert ele_obtained is not None
        assert len(ele_obtained) == 0
