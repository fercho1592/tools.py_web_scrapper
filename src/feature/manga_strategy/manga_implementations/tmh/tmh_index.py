from feature_interfaces.web_drivers.enums import CommonAttrs as COMMON_ATTRS
from feature_interfaces.web_drivers.enums import CommonTags as COMMON_TAGS
from feature_interfaces.strategies.i_manga_strategy import IMangaPage, IMangaIndex
from feature.manga_strategy.manga_implementations._base_strategy import BaseMangaIndex
from feature_interfaces.web_drivers.i_web_element_driver import IWebElementDriver


class TmhMangaIndex(BaseMangaIndex, IMangaIndex):
    def get_manga_name(self) -> str:
        title = self.DomReader.query_selector(".panel.panel-primary.panel-title h3")
        return title.get_value() if title is not None else ""

    def _get_index_page(self, index_page: int) -> IMangaIndex:
        del index_page
        return self

    def get_manga_page_async(self, page: int = 0) -> IMangaPage:
        page = page if page > 0 else 1
        sel_page = self.DomReader.query_selector_all(".well a")
        if page > len(sel_page):
            return None
        return self.Strategy.get_page_from_url_async(
            sel_page[page - 1].get_attr_value(COMMON_ATTRS.HREF)
        )

    def _get_manga_data_elements(self) -> list[IWebElementDriver]:
        form_data = self.DomReader.query_selector("#form-favorite-author")
        if form_data is None or form_data.Parent is None:
            return []
        return form_data.Parent.query_selector_all("ul")

    def get_manga_genders(self) -> list[str]:
        result = []
        data_elements = self._get_manga_data_elements()
        for ele in data_elements:
            li_elements = ele.get_children_by_tag(COMMON_TAGS.LI)
            if li_elements[0].Children[0].get_value() in ["Genders", "Tags"]:
                anchors = ele.get_children_by_tag(COMMON_TAGS.ANCHOR)
                result.extend([ele.get_value() for ele in anchors if ele.get_value()])
        return result

    def get_manga_artist(self) -> list[str]:
        data_elements = self._get_manga_data_elements()
        for ele in data_elements:
            li_elements = ele.get_children_by_tag(COMMON_TAGS.LI)
            if li_elements[0].Children[0].get_value() == "Artists and Artists Groups":
                anchors = li_elements[1].get_children_by_tag(COMMON_TAGS.ANCHOR)
                return [ele.get_value() for ele in anchors]
        return []

    # TODO: Unit Tests
    def get_manga_group(self) -> list[str]:
        data_elements = self._get_manga_data_elements()
        for ele in data_elements:
            li_elements = ele.get_children_by_tag(COMMON_TAGS.LI)
            if li_elements[0].Children[0].get_value() == "Uploaded By":
                result = [
                    ele.Children[0].Value
                    for ele in li_elements[1:]
                    if ele.Children[0] is not None
                    and ele.Children[0].Value != ""
                    and ele.Children[0].Value is not None
                ]
                return result
        return []
