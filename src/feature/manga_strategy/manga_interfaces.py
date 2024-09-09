'''Defines interfaces to be used by each strategy depending on the url domain'''

from abc import ABC, abstractmethod
from typing import Self

class IMangaPage(ABC):
  '''Interface of a Manga Page'''
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
  def get_next_page_async(self) -> Self:
    pass
  @abstractmethod
  def is_last_page(self) -> bool:
    pass
  @abstractmethod
  def _get_next_image_url(self) -> str:
    pass
  @abstractmethod
  def get_manga_name(self) -> str:
    pass

class IMangaIndex(ABC):
  '''Interface that represent index page'''
  @abstractmethod
  def get_index_page_cout(self) -> str:
    pass
  @abstractmethod
  def get_manga_page_count(self) -> str:
    pass
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

class IMangaStrategy(ABC):
  ''' Main Class for strategi'''
  @staticmethod
  @abstractmethod
  def is_from_domain(url:str) -> bool:
    pass
  @staticmethod
  @abstractmethod
  def create_strategy(url:str) -> Self:
    pass
  @abstractmethod
  def get_first_page(
    self, page_number: int = 0, index_page: int = 0) -> IMangaPage:
    pass
  @abstractmethod
  def get_page_from_url_async(self, url: str) -> IMangaPage:
    pass
