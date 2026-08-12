from typing import Protocol
from contracts.strategies.i_manga_strategy import IMangaStrategy

class MangaFactoryProtocol(Protocol):
    def get_manga_strategy(self, url:str) -> IMangaStrategy: ...
