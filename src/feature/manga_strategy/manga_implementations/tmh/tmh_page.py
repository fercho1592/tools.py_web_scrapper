'''File for tmh page class'''
from feature.manga_strategy.manga_interfaces import IMangaPage
from feature.manga_strategy.manga_implementations._base_strategy import BaseMangaPage
import enums.common_attrs as COMMON_ATTRS
import enums.common_tags as COMMON_TAGS

class TmhMangaPage(BaseMangaPage,IMangaPage):
  '''Define a page object for tmh web page'''

  def get_img_url(self) -> tuple[str, dict[str,str]]:
    image_eles = self.reader.get_by_tag_name(COMMON_TAGS.IMG,
      COMMON_ATTRS.CLASS, "content-image lazy")
    if len(image_eles) == 0:
      raise NotImplementedError("Image not found")
    url = image_eles[0].get_attr_value(COMMON_ATTRS.DATA_ORIGINAL)
    return url, { "referer": self.url }

  def get_image_name(self) -> str:
    image_eles = self.reader.get_by_attrs(
      COMMON_ATTRS.CLASS, "content-image lazy")
    if len(image_eles) == 0:
      raise NotImplementedError("Image not found")
    image_name = image_eles[0].get_attr_value(COMMON_ATTRS.DATA_ORIGINAL)
    return image_name.split("/")[-1]

  def get_image_number(self) -> tuple[str,str]:
    page_selector = self.reader.get_by_attrs(COMMON_ATTRS.ID, "select-page")[0]
    selected = page_selector.get_children_by_tag(
      COMMON_TAGS.OPTION, COMMON_ATTRS.SELECTED, "selected")[0]
    selected = page_selector.get_children_by_tag(
      COMMON_TAGS.OPTION)[-1]
    return (selected.get_value(), selected.get_value())

  def get_next_page_async(self) -> IMangaPage:
    image_eles = self.reader.get_by_attrs(
      COMMON_ATTRS.CLASS, "content-image lazy")
    if len(image_eles) == 0:
      raise NotImplementedError("Image not found")
    url = image_eles[0].parent.get_attr_value(COMMON_ATTRS.HREF)
    return self.web_scrapper.get_page_from_url_async(url)

  def is_last_page(self) -> bool:
    image_eles = self.reader.get_by_attrs(
      COMMON_ATTRS.CLASS, "content-image lazy")
    if len(image_eles) == 0:
      raise NotImplementedError("Image not found")
    return image_eles[0].parent.tag != COMMON_TAGS.ANCHOR

  def get_manga_name(self) -> str:
    header_name = self.reader.get_by_attrs(
      COMMON_ATTRS.CLASS, "reader-title")[0]
    return header_name.get_value()
