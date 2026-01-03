'''Set up all manga implementations'''
from typing import Tuple, Type
from feature_interfaces.enums.settings_enum import ConfigEnum
from feature_interfaces.protocols.config_protocol import ConfigServiceProtocol, LoggerProtocol
from feature_interfaces.services.http_service import IHttpService
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy
from feature.manga_strategy.manga_implementations.tmh import tmh_strategy
from feature.manga_strategy.manga_implementations.e_web import e_web_strategy
from feature.container import Container

class StrategyFactory:
    MANGA_IMPLEMENTATIONS:list[Tuple[Type[IMangaStrategy], str]] = [
        (e_web_strategy.EMangaStrategy, ConfigEnum.E_MANGA_DOMAIN),
        (tmh_strategy.TmhMangaStrategy, ConfigEnum.TMH_MANGA_DOMAIN)
    ]

    def __init__(self, config_manager: ConfigServiceProtocol, container: Container) -> None:
        self.config_manager:ConfigServiceProtocol = config_manager
        self.container:Container = container

    def get_manga_strategy(self, url:str) -> IMangaStrategy:
        for (typeStartegy, config_key) in StrategyFactory.MANGA_IMPLEMENTATIONS:
            if self.is_from_domain((typeStartegy, config_key), url):
                return typeStartegy(url, self.container.resolve_factory(LoggerProtocol, typeStartegy.__name__), self.container.resolve(IHttpService))
        raise Exception(f"No strategy found for url: {url}")

    def is_from_domain(self, strategyImpl, url:str) -> bool:
        config = self.config_manager.get_config_value(strategyImpl[1])
        return url.startswith(config)