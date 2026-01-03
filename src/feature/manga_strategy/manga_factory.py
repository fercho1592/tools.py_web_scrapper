from feature_interfaces.protocols.factory_protocol import MangaFactoryProtocol
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy

class MangaFactory(MangaFactoryProtocol):
    def __init__(self, types: list[IMangaStrategy]):
        self.__types = types

    def get_manga_strategy(self, url:str) -> IMangaStrategy:
        for manga_strategy in self.__types:
            if manga_strategy.is_from_domain(url):
                return manga_strategy.create_strategy(url)

        raise NotImplementedError()
