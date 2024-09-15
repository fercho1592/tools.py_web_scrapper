'''Module for tmh index pages'''
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

