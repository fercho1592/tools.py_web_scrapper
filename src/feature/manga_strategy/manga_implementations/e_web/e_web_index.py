from feature.manga_strategy.manga_interfaces import IMangaPage, IMangaIndex
from feature.manga_strategy.manga_implementations._base_strategy import BaseMangaIndex
import feature.html_reader.common_attrs as COMMON_ATTRS
import feature.html_reader.common_tags as COMMON_TAGS
from feature.html_reader.dom_reader import HtmlElement

class EMangaIndex(BaseMangaIndex,IMangaIndex):
    '''Class that represent index page'''
    @staticmethod
    def get_max_pages_in_index() -> int:
        return 40

    def get_manga_name(self) -> str:
        name_element = self.dom_reader.get_by_attrs(COMMON_ATTRS.ID, "gn")[0]
        manga_name = name_element.get_value()
        ## fix Manga name
        return manga_name

    def _get_index_page(self, index_page: int) -> IMangaIndex:
        self._logger.info("Getting Index page# [%s]", index_page)
        return self.strategy.get_index_page_async(index_page)

    def get_manga_page_async(self, page:int = 0) -> IMangaPage:
        page = 1 if page < 1 else page
        max_page_count = self.get_max_pages_in_index()
        index_page = page // max_page_count
        index = self._get_index_page(index_page) if page > max_page_count else self
        real_page = page - (index_page * max_page_count)
        pages = index.dom_reader.get_by_attrs(COMMON_ATTRS.CLASS, "gdtm")
        page_to_search = pages[real_page-1]
        page_children = page_to_search.get_children_by_tag(COMMON_TAGS.ANCHOR)

        new_page = index.strategy.get_page_from_url_async(
        page_children[0].get_attr_value(COMMON_ATTRS.HREF))
        return new_page

    def _get_manga_data_elements(self) -> list[HtmlElement]:
        taglist = self.dom_reader.get_by_attrs(COMMON_ATTRS.ID, "taglist")[0]
        children = taglist.get_children_by_tag(COMMON_TAGS.TR)
        return children

    def get_manga_genders(self) -> list[str]:
        data_elements = self._get_manga_data_elements()
        for ele in data_elements:
            li_elements = ele.get_children_by_tag(COMMON_TAGS.TD)
            if li_elements[0].get_value() == "female:":
                tags = ele.get_children_by_tag(COMMON_TAGS.ANCHOR)
                return [ele.value for ele in tags]
        return []

    def get_manga_artist(self) -> list[str]:
        data_elements = self._get_manga_data_elements()
        for ele in data_elements:
            li_elements = ele.get_children_by_tag(COMMON_TAGS.TD)
            if li_elements[0].get_value() == "artist:":
                tags = ele.get_children_by_tag(COMMON_TAGS.ANCHOR)
                return [ele.value for ele in tags]
        return []

    def get_manga_group(self) -> list[str]:
        data_elements = self._get_manga_data_elements()
        for ele in data_elements:
            li_elements = ele.get_children_by_tag(COMMON_TAGS.TD)
            if li_elements[0].get_value() == "group:":
                tags = ele.get_children_by_tag(COMMON_TAGS.ANCHOR)
                return [ele.value for ele in tags]
        return []
