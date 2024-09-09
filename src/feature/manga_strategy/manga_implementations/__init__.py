'''Definition of each manga implementation'''
from manga_strategy.manga_interfaces import IMangaStrategy
from . import e_web_strategy

MANGA_IMPLEMENTATIONS:list[IMangaStrategy] = [
  e_web_strategy.EMangaStrategy
]
