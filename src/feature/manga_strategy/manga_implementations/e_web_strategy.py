'''Module for implementation for e-hentai pages'''
from typing import Self
from manga_strategy.manga_interfaces import IMangaStrategy, IMangaIndex, IMangaPage
import infrastructure.my_logger as my_logger
import infrastructure.http_service as http_service
from html_reader.html_decoder import HtmlDecoder
from html_reader.dom_reader import DomElement
import enums.common_attrs as COMMON_ATTRS
import enums.common_tags as COMMON_TAGS
import re
import time

__logger = my_logger.get_logger(__name__)
def DefaultViewTimer():
  delay_seconds = 5
  __logger.debug("Delay of [%s] seconds", delay_seconds)
  time.sleep(delay_seconds)

class EMangaStrategy(IMangaStrategy):
  '''Implementation for e-hentai page'''
  @staticmethod
  def is_from_domain(url:str) -> bool:
    # get from settings
    return url.startswith("https://e-hentai.org")

  def __init__(self, web_page: str):
    #self.__logger = my_logger.get_logger(__name__)
    self._web_page = web_page

  def get_first_page(self, page_number: int) -> IMangaPage:
    dom_element = self._get_dom_component(self._web_page)
    # Identify if is a page or index
    is_index_page = len(dom_element.get_by_attrs(COMMON_ATTRS.ID, "gn")) == 0

    if is_index_page is False:
      return EMangaPage(self, dom_element, self._web_page)

    # create index page
    index_page = EMangaIndex(self, dom_element)
    return index_page.get_manga_page_async(page_number)

  def get_index_page_async(self, index_page = 0) -> IMangaIndex:
    dom_reader = self._get_dom_component(f"{self._web_page}?p={index_page}")

    DefaultViewTimer()
    return EMangaIndex(self, dom_reader)

  def get_page_from_url_async(self, url: str) -> IMangaPage:
    dom_reader = self._get_dom_component(url)
    DefaultViewTimer()
    return EMangaPage(self, dom_reader, url)

  def _get_dom_component(self, url: str):
    html = http_service.get_html_from_url(url)
    decoder = HtmlDecoder()
    decoder.set_html(html)
    return decoder.get_dom_component()

class EMangaIndex(IMangaIndex):
  '''Class that represent index page'''
  def __init__(self, strategy: IMangaStrategy,dom_reader: DomElement) -> None:
    super().__init__()
    self.strategy = strategy
    self.dom_reader = dom_reader
    self._logger = my_logger.get_logger(__name__)

  def get_index_page_cout(self) -> str:
    index_table = self.dom_reader.get_by_attrs(COMMON_ATTRS.CLASS,"ptt")
    page_ancors = index_table[0].get_children_by_tag(
      COMMON_TAGS.ANCHOR, COMMON_ATTRS.HREF
      )
    page_ancors_count = len(page_ancors)
    if page_ancors_count == 1:
      return 1

    return page_ancors[page_ancors_count-2].value

  def get_manga_page_count(self) -> str:
    manga_detail_elements = self.dom_reader.get_by_attrs(
      COMMON_ATTRS.ID, "gdd")[0].get_children_by_tag(COMMON_TAGS.TR)
    for ele in manga_detail_elements:
      if ele.children[0].get_value() == "Length:":
        return ele.children[1].get_value()

  @staticmethod
  def get_max_pages_in_index() -> int:
    return 40

  def get_manga_name(self) -> str:
    name_element = self.dom_reader.get_by_attrs(COMMON_ATTRS.ID, "gn")[0]
    manga_name = name_element.get_value()
    ## fix Manga name
    return manga_name

  def _get_index_page(self, index_page: int) -> Self:
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
    DefaultViewTimer()
    return new_page

class EMangaPage(IMangaPage):
  '''Structure in case of a EManga Page'''
  def __init__(
      self, web_scrapper:IMangaStrategy, dom_reader:DomElement, url: str):
    self.web_scrapper = web_scrapper
    self.reader = dom_reader
    self.url:str = url
    self.image_name:str = None
    self.image_number:int = None
    self._logger = my_logger.get_logger(__name__)

  def get_img_url(self) -> str:
    self._logger.debug("Getting image url from [%s]", self.url)
    imgs = self.reader.get_by_attrs(COMMON_ATTRS.ID, "img")
    img = imgs[0]

    return img.get_attr_value(COMMON_ATTRS.SRC)

  def get_image_name(self) -> str:
    if self.image_name is not None:
      return self.image_name
    divs = self.reader.get_by_attrs(COMMON_ATTRS.ID, "i2")
    img_details_ele = divs[0].children[1]
    details = img_details_ele.get_value()
    det_array:list[str] = re.split("::", details)

    self.image_name = det_array[0].strip()
    return self.image_name

  def get_image_number(self) -> str:
    if self.image_number is not None:
      return self.image_number
    div = self.reader.get_by_attrs(COMMON_ATTRS.ID, "i2")[0]
    img_details_ele = div.get_children_by_tag(COMMON_TAGS.SPAM)

    self.image_number = (
       img_details_ele[0].get_value().strip(),
       img_details_ele[1].get_value().strip()
       )
    return self.image_number

  def get_next_page_async(self) -> Self:
    next_page_url = self._get_next_image_url()
    new_page = self.web_scrapper.get_page_from_url_async(next_page_url)
    DefaultViewTimer()

    return new_page

  def is_last_page(self) -> bool:
    next_page_url = self._get_next_image_url()
    return self.url == next_page_url

  def _get_next_image_url(self) -> str:
    imgs = self.reader.get_by_attrs(COMMON_ATTRS.ID, "img")
    img = imgs[0]
    next_page_component = img.parent
    return next_page_component.get_attr_value(COMMON_ATTRS.HREF)

  def get_manga_name(self) ->str:
    pass
