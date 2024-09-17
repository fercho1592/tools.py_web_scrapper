'''Module for tmh index pages'''
from feature.html_reader.dom_reader import HtmlElement
from feature.manga_strategy.manga_interfaces import IMangaPage, IMangaIndex
from feature.manga_strategy.manga_implementations._base_strategy import BaseMangaIndex
import feature.html_reader.common_attrs as COMMON_ATTRS
import feature.html_reader.common_tags as COMMON_TAGS

class TmhMangaIndex(BaseMangaIndex,IMangaIndex):
  '''Class for tmh manga index'''
  @staticmethod
  def get_max_pages_in_index() -> int:
    return 100

  def get_manga_name(self) -> str:
    divs = self.dom_reader.get_by_attrs(
      COMMON_ATTRS.CLASS, valule="panel panel-primary panel-title")
    if len(divs) == 0:
      return ""
    h3 = divs[0].get_children_by_tag(COMMON_TAGS.H3)
    return h3[0].get_value() if len(h3) != 0 else ""

  def _get_index_page(self, index_page: int) -> IMangaIndex:
    del index_page
    return self

  def get_manga_page_async(self, page:int = 0) -> IMangaPage:
    page = page if page > 0 else 1
    image_divs = self.dom_reader.get_by_attrs(COMMON_ATTRS.CLASS, "well")
    if len(image_divs) == 0:
      return None
    anchors_eles = image_divs[0].get_children_by_tag(COMMON_TAGS.ANCHOR)
    sel_page = anchors_eles[page - 1]
    return self.strategy.get_page_from_url_async(
      sel_page.get_attr_value(COMMON_ATTRS.HREF))

  def _get_manga_data_elements(self) -> list[HtmlElement]:
    form_data = self.dom_reader.get_by_attrs(
      COMMON_ATTRS.ID, "form-favorite-author"
    )[0]
    parent = form_data.parent
    return parent.get_children_by_tag(COMMON_TAGS.UL)

  def get_manga_genders(self) -> list[str]:
    data_elements = self._get_manga_data_elements()
    for ele in data_elements:
      li_elements = ele.get_children_by_tag(COMMON_TAGS.LI)
      if li_elements[0].children[0].get_value() == "Genders":
        return [ele.children[0].value for ele in li_elements[1:]]
    return []

  def get_manga_artist(self) -> list[str]:
    data_elements = self._get_manga_data_elements()
    for ele in data_elements:
      li_elements = ele.get_children_by_tag(COMMON_TAGS.LI)
      if li_elements[0].children[0].get_value() == "Artists and Artists Groups":
        return [ele.children[0].value for ele in li_elements[1:]]
    return []

  def get_manga_group(self) -> list[str]:
    data_elements = self._get_manga_data_elements()
    for ele in data_elements:
      li_elements = ele.get_children_by_tag(COMMON_TAGS.LI)
      if li_elements[0].children[0].get_value() == "Uploaded By":
        return [ele.children[0].value for ele in li_elements[1:]]
    return []
