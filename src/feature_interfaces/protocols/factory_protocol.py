from typing import Protocol
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy

class MangaFactoryProtocol(Protocol):
    def get_manga_strategy(self, url:str) -> IMangaStrategy: ...
