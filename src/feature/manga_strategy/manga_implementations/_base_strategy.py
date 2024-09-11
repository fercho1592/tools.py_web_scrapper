'''Module for implementation for e-hentai pages'''
from typing import Self
from feature.manga_strategy.manga_interfaces import IMangaStrategy, IMangaIndex, IMangaPage
from feature.html_reader.html_decoder import HtmlDecoder
from feature.html_reader.dom_reader import DomElement
import infrastructure.my_logger as my_logger
import infrastructure.http_service as http_service
import time

from abc import abstractmethod

def DefaultViewTimer():
  delay_seconds = 5
  #__logger.debug("Delay of [%s] seconds", delay_seconds)
  time.sleep(delay_seconds)

class BaseStrategy(IMangaStrategy):
  '''Implementation for e-hentai page'''
  @staticmethod
  @abstractmethod
  def is_from_domain(url:str) -> bool:
    pass

  @staticmethod
  @abstractmethod
  def create_strategy(url:str) -> IMangaStrategy:
    pass

  def __init__(self, web_page: str):
    self._logger = my_logger.get_logger(__name__)
    self._web_page = web_page

  def _get_dom_component(self, url: str):
    html = http_service.get_html_from_url(url)
    decoder = HtmlDecoder()
    decoder.set_html(html)
    return decoder.get_dom_component()

  @abstractmethod
  def get_page_from_url_async(self, url: str) -> IMangaPage:
    pass

  @abstractmethod
  def get_first_page(self, page_number: int) -> IMangaPage:
    pass

  @abstractmethod
  def get_index_page_async(self, index_page = 0) -> IMangaIndex:
    pass

class BaseMangaIndex(IMangaIndex):
  '''Class that represent index page'''
  def __init__(self, strategy: IMangaStrategy,dom_reader: DomElement) -> None:
    super().__init__()
    self.strategy = strategy
    self.dom_reader = dom_reader
    self._logger = my_logger.get_logger(__name__)

  @staticmethod
  @abstractmethod
  def get_max_pages_in_index() -> int:
    pass

  @abstractmethod
  def get_manga_name(self) -> str:
    pass

  @abstractmethod
  def _get_index_page(self, index_page: int) -> Self:
    pass

  @abstractmethod
  def get_manga_page_async(self, page:int = 0) -> IMangaPage:
    pass

class BaseMangaPage(IMangaPage):
  '''Structure in case of a EManga Page'''
  def __init__(
      self, web_scrapper:IMangaStrategy, dom_reader:DomElement, url: str):
    self.web_scrapper = web_scrapper
    self.reader = dom_reader
    self.url:str = url
    self.image_name:str = None
    self.image_number:int = None
    self._logger = my_logger.get_logger(__name__)

  @abstractmethod
  def get_img_url(self) -> str:
    pass

  @abstractmethod
  def get_image_name(self) -> str:
    pass

  @abstractmethod
  def get_image_number(self) -> str:
    pass

  @abstractmethod
  def get_manga_name(self) ->str:
    pass
