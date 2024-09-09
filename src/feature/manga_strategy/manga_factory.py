'''Factory to select wich manga implementation will be used'''
from manga_implementations import MANGA_IMPLEMENTATIONS
from manga_interfaces import IMangaStrategy

class MangaFactory:
  @staticmethod
  def get_manga_strategy(url:str) -> IMangaStrategy:
    for manga_strategy in MANGA_IMPLEMENTATIONS:
      if manga_strategy.is_from_domain(url):
        return manga_strategy

    raise NotImplementedError()
