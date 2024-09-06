''' Strategy for e-hentay service'''
from enums.common_tags import COMMON_ATTRS, COMMON_TAGS
import infrastructure.http_service as HttpService
import infrastructure.my_logger as myLogger
from html_reader.html_decoder import HtmlDecoder
from html_reader.dom_reader import DomElement
import re
import time

__logger = myLogger.get_logger(__name__)

def DefaultViewTimer():
  delay_seconds = 5
  __logger.debug("Delay of [%s] seconds", delay_seconds)
  time.sleep(delay_seconds)

class EWebScraper:
  ''' Main Class for strategi'''
  def __init__(self, web_page: str, manga_page_number = 0):
    del manga_page_number
    #self.__page_number = manga_page_number
    #self.__logger = myLogger.get_logger(__name__)
    self.__web_page = web_page

  def get_index_page_async(self, index_page = 0):
    html = HttpService.get_html_from_url(f"{self.__web_page}?p={index_page}")
    decoder = HtmlDecoder()
    decoder.set_html(html)
    dom_reader = decoder.get_dom_component()

    DefaultViewTimer()
    return _EIndex(self, dom_reader)

  def get_page_async(self):
    html = HttpService.get_html_from_url(f"{self.__webPage}")
    decoder = HtmlDecoder()
    decoder.set_html(html)
    dom_reader = decoder.get_dom_component()

    DefaultViewTimer()
    return _EMangaPage(self, dom_reader, self.__webPage)

  def get_page_from_index_async(self, url):
    html = HttpService.get_html_from_url(url)
    decoder = HtmlDecoder()
    decoder.set_html(html)
    dom_reader = decoder.get_dom_component()

    return _EMangaPage(self, dom_reader, url)

class _EIndex:
  '''Class that represent index page'''
  def __init__(self, web_scrapper:EWebScraper, dom_reader:DomElement):
    self.web_scrapper = web_scrapper
    self.reader = dom_reader
    self.__logger = myLogger.get_logger(__name__)

  def get_index_page_cout(self):
    index_table = self.reader.get_by_attrs(COMMON_ATTRS.CLASS,"ptt")
    page_ancors = index_table[0].get_children_by_tag(
      COMMON_TAGS.ANCHOR, COMMON_ATTRS.HREF
      )
    page_ancors_count = len(page_ancors)
    if page_ancors_count == 1:
      return 1

    return page_ancors[page_ancors_count-2].value

  def get_manga_page_count(self):
    manga_detail_elements = self.reader.get_by_attrs(
      COMMON_ATTRS.ID, "gdd")[0].GetChildrenByTag(COMMON_TAGS.TR)
    for ele in manga_detail_elements:
      if ele.children[0].getValue() == "Length:":
        return ele.children[1].getValue()

  def get_max_pages_in_index(self):
    return 40

  def get_manga_name(self):
    name_element = self.reader.get_by_attrs(COMMON_ATTRS.ID, "gn")[0]
    return name_element.getValue()

  def __get_index_page(self, index_page):
    self.__logger.info("Getting Index page# [%s]", index_page)
    return self.webScrapper.getIndexPageAsync(index_page)

  def get_manga_page_async(self, page = 0):
    page = 1 if page < 1 else page
    max_page_count = self.get_max_pages_in_index()
    index_page = page // max_page_count
    index = self.__getIndexPage(index_page) if page > max_page_count else self
    real_page = page - (index_page * max_page_count)
    pages = index.reader.get_by_attrs(COMMON_ATTRS.CLASS, "gdtm")
    page_to_search = pages[real_page-1]
    page_children = page_to_search.GetChildrenByTag(COMMON_TAGS.ANCHOR)

    new_page = index.webScrapper.getPageFromIndexAsync(
      page_children[0].get_attr_value(COMMON_ATTRS.HREF))
    DefaultViewTimer()
    return new_page

class _EMangaPage:
  '''Structure in case of a Manga Page'''
  def __init__(self, web_scrapper, dom_reader, url):
    self.web_scrapper = web_scrapper
    self.reader = dom_reader
    self.url:str = url
    self.image_name:str = None
    self.image_number:int = None
    self.__logger = myLogger.get_logger(__name__)

  def get_img_url(self):
    self.__logger.debug("Getting image url from [%s]", self.url)
    imgs = self.reader.get_by_attrs(COMMON_ATTRS.ID, "img")
    img = imgs[0]

    return img.get_attr_value(COMMON_ATTRS.SRC)

  def get_image_name(self):
    if self.image_name is not None:
      return self.image_name
    divs = self.reader.get_by_attrs(COMMON_ATTRS.ID, "i2")
    img_details_ele = divs[0].children[1]
    details = img_details_ele.getValue()
    det_array = re.split("::", details)

    self.image_name = det_array[0].strip()
    return self.image_name

  def get_image_number(self):
    if self.image_number is not None:
      return self.image_number
    div = self.reader.get_by_attrs(COMMON_ATTRS.ID, "i2")[0]
    img_details_ele = div.GetChildrenByTag(COMMON_TAGS.SPAM)

    self.image_number = (
       img_details_ele[0].get_value().strip(),
       img_details_ele[1].get_value().strip()
       )
    return self.image_number

  def get_next_page_async(self):
    next_page_url = self.__get_next_image_url()
    new_page = self.webScrapper.getPageFromIndexAsync(next_page_url)
    DefaultViewTimer()

    return new_page

  def is_last_page(self):
    next_page_url = self.__get_next_image_url()
    return self.url == next_page_url

  def __get_next_image_url(self):
    imgs = self.reader.get_by_attrs(COMMON_ATTRS.ID, "img")
    img = imgs[0]
    next_page_component = img.parent
    return next_page_component.get_attr_value(COMMON_ATTRS.HREF)
