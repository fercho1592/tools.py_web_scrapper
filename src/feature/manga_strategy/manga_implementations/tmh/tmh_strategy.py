'''Module for tmh strategy'''
import feature.html_reader.common_attrs as COMMON_ATTRS

from feature.manga_strategy.manga_implementations._base_strategy import BaseStrategy, DefaultViewTimer
from feature.manga_strategy.manga_implementations.tmh.tmh_index import TmhMangaIndex
from feature.manga_strategy.manga_implementations.tmh.tmh_page import TmhMangaPage
from feature.manga_strategy.manga_interfaces import IMangaStrategy, IMangaPage, IMangaIndex

import infrastructure.config_manager as config_manager

class TmhMangaStrategy(BaseStrategy, IMangaStrategy):
  '''Define a page object for tmh strategy'''
  @staticmethod
  def is_from_domain(url:str) -> bool:
    config = config_manager.read_config()
    return url.startswith(config["tmh_manga_domain"])

  @staticmethod
  def create_strategy(url:str) -> IMangaStrategy:
    return TmhMangaStrategy(url)

  def get_first_page(self, page_number: int) -> IMangaPage:
    dom_element = self._get_dom_component(self._web_page)
    # Identify if is a page or index
    is_index_page = len(
      dom_element.get_by_attrs(COMMON_ATTRS.ID, "content-images")) == 0

    if is_index_page is False:
      self._logger.debug("Creating an object Page for [%s]", self._web_page)
      return TmhMangaPage(self, dom_element, self._web_page)

    # create index page
    self._logger.debug("Creating an object Index for [%s]", self._web_page)
    index_page = TmhMangaIndex(self, dom_element)
    return index_page.get_manga_page_async(page_number)

  def get_index_page_async(self, index_page = 0) -> IMangaIndex:
    del index_page
    dom_reader = self._get_dom_component(self._web_page)
    DefaultViewTimer()
    return TmhMangaIndex(self, dom_reader)

  def get_page_from_url_async(self, url: str) -> IMangaPage:
    dom_reader = self._get_dom_component(url)
    DefaultViewTimer()
    return TmhMangaPage(self, dom_reader, url)
