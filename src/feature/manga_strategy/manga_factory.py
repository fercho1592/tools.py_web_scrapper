'''Factory to select wich manga implementation will be used'''
from feature.manga_strategy.manga_implementations.container import MANGA_IMPLEMENTATIONS
from feature_interfaces.strategies.manga_interfaces import IMangaStrategy

class MangaFactory:
    @staticmethod
    def get_manga_strategy(url:str) -> IMangaStrategy:
        for manga_strategy in MANGA_IMPLEMENTATIONS:
            if manga_strategy.is_from_domain(url):
                return manga_strategy.create_strategy(url)

        raise NotImplementedError()
