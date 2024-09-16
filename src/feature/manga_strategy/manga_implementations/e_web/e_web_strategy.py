'''Module for implementation for e-hentai pages'''
import feature.html_reader.common_attrs as COMMON_ATTRS
import configs.config_manager as config_manager
from feature.manga_strategy.manga_implementations._base_strategy import BaseStrategy, DefaultViewTimer
from feature.manga_strategy.manga_interfaces import IMangaStrategy, IMangaIndex, IMangaPage
from feature.manga_strategy.manga_implementations.e_web.e_web_index import EMangaIndex
from feature.manga_strategy.manga_implementations.e_web.e_web_page import EMangaPage

class EMangaStrategy(BaseStrategy,IMangaStrategy):
  '''Implementation for e-hentai page'''
  @staticmethod
  def is_from_domain(url:str) -> bool:
    config = config_manager.read_config()
    return url.startswith(config["e_manga_domain"])

  @staticmethod
  def create_strategy(url:str) -> IMangaStrategy:
    return EMangaStrategy(url)

  def get_first_page(self, page_number: int) -> IMangaPage:
    dom_element = self._get_dom_component(self._web_page)
    # Identify if is a page or index
    is_index_page = len(dom_element.get_by_attrs(COMMON_ATTRS.ID, "gn")) == 0

    if is_index_page is True:
      self._logger.debug("Creating an object Page for [%s]", self._web_page)
      return EMangaPage(self, dom_element, self._web_page)

    # create index page
    self._logger.debug("Creating an object Index for [%s]", self._web_page)
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
