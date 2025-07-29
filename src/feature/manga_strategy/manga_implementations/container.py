'''Set up all manga implementations'''
from typing import Type
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy
from feature.manga_strategy.manga_implementations.tmh import tmh_strategy
from feature.manga_strategy.manga_implementations.e_web import e_web_strategy

MANGA_IMPLEMENTATIONS:list[Type[IMangaStrategy]] = [
    e_web_strategy.EMangaStrategy,
    tmh_strategy.TmhMangaStrategy
]
