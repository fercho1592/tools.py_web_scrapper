from feature_interfaces.enums.settings_enum import ConfigEnum
from feature_interfaces.protocols.config_protocol import ConfigServiceProtocol, LoggerProtocol
from feature_interfaces.services.http_service import IHttpService
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy

from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature.image_converter.pillow_image_converter import PillowImageConverter
from feature.image_converter.image_converter_interfaces import IImageEditorService
from feature.container import Container
from feature.manga_strategy.manga_implementations.container import StrategyFactory
from infrastructure.http_service import HttpService

from configs.config_manager import ConfigParserService, EnvironConfig
from configs.logger_factory import LoggerFactory

def build_container():

    container = Container()
    container.register(IHttpService, lambda: HttpService(container.resolve_factory(LoggerProtocol, HttpService.__name__)))
    container.register(ConfigServiceProtocol, __env_service_factory, is_singleton=True)
    container.register(IImageEditorService, lambda: PillowImageConverter(container.resolve_factory(LoggerProtocol, PillowImageConverter.__name__)))

    container.register_factory(MangaScraper, lambda url: MangaScraper(
        container.resolve_factory(IMangaStrategy, url),
        container.resolve_factory(LoggerProtocol, MangaScraper.__name__),
        container.resolve(IHttpService)))
    container.register(StrategyFactory, lambda: StrategyFactory(container))
    container.register_factory(IMangaStrategy, lambda url: container.resolve(StrategyFactory).get_manga_strategy(url))
    container.register_factory(LoggerProtocol, lambda name: LoggerFactory().get_logger(name))

    return container

def __env_service_factory():
    environService = EnvironConfig()
    if environService.get_config_value(ConfigEnum.E_MANGA_DOMAIN):
        return environService
    return ConfigParserService()