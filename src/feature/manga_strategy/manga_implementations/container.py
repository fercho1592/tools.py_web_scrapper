'''Set up all manga implementations'''
from feature.manga_strategy.manga_interfaces import IMangaStrategy
from feature.manga_strategy.manga_implementations.tmh import tmh_strategy
from .e_web import e_web_strategy

MANGA_IMPLEMENTATIONS:list[IMangaStrategy] = [
  e_web_strategy.EMangaStrategy,
  tmh_strategy.TmhMangaStrategy
]
