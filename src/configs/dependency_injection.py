from feature_interfaces.enums.settings_enum import ConfigEnum
from feature_interfaces.protocols.config_protocol import (
    ConfigServiceProtocol,
    LoggerProtocol,
)
from feature_interfaces.services.http_service import IHttpService
from feature_interfaces.services.webdav_service import WebDAVService
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy
from feature_interfaces.services.pdf_creator import IPdfCreator

from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature.image_converter.pillow_image_converter import PillowImageConverter
from feature.image_converter.image_converter_interfaces import IImageEditorService
from feature.container import Container
from feature.manga_strategy.manga_implementations.container import StrategyFactory
from handler.image_converter_handler import ImageConverterHandler
from handler.manga_downloader_handler import MangaDownloaderHandler
from handler.pdf_creator_handler import PDFCreatorHandler
from handler.webdav_handler import WebDavHandler
from infrastructure.http_service import HttpService

from configs.config_manager import ConfigParserService, EnvironConfig
from configs.logger_factory import LoggerFactory
from infrastructure.pdf_generator import PdfCreator


def build_container():

    container = Container()
    container.register(
        IHttpService,
        lambda: HttpService(
            container.resolve_factory(LoggerProtocol, HttpService.__name__)
        ),
    )
    container.register(ConfigServiceProtocol, __env_service_factory, is_singleton=True)
    container.register(
        IImageEditorService,
        lambda: PillowImageConverter(
            container.resolve_factory(LoggerProtocol, PillowImageConverter.__name__)
        ),
    )
    container.register(
        IPdfCreator,
        lambda: PdfCreator(
            container.resolve(IImageEditorService),
            container.resolve_factory(LoggerProtocol, PdfCreator.__name__),
        ),
    )

    container.register_factory(
        MangaScraper,
        lambda url: MangaScraper(
            container.resolve_factory(IMangaStrategy, url),
            container.resolve_factory(LoggerProtocol, MangaScraper.__name__),
            container.resolve(IHttpService),
        ),
    )
    container.register(StrategyFactory, lambda: StrategyFactory(container))
    container.register_factory(
        IMangaStrategy,
        lambda url: container.resolve(StrategyFactory).get_manga_strategy(url),
    )
    container.register_factory(
        LoggerProtocol, lambda name: LoggerFactory().get_logger(name)
    )
    container.register(
        WebDAVService,
        lambda: WebDAVService(
            container.resolve_factory(LoggerProtocol, WebDAVService.__name__),
            container.resolve(ConfigServiceProtocol).get_config_value(
                ConfigEnum.E_WEBDAV_URL
            ),
            container.resolve(ConfigServiceProtocol).get_config_value(
                ConfigEnum.E_WEBDAV_USER
            ),
            container.resolve(ConfigServiceProtocol).get_config_value(
                ConfigEnum.E_WEBDAV_PASSWORD
            ),
        ),
    )

    container.register(
        ImageConverterHandler,
        lambda: ImageConverterHandler(
            container.resolve_factory(LoggerProtocol, ImageConverterHandler.__name__),
            container.resolve(IImageEditorService),
        ),
    )
    container.register(
        WebDavHandler,
        lambda: WebDavHandler(
            container.resolve_factory(LoggerProtocol, WebDavHandler.__name__),
            container.resolve(WebDAVService),
        ),
    )
    container.register(
        MangaDownloaderHandler,
        lambda: MangaDownloaderHandler(
            container.resolve_factory(LoggerProtocol, MangaDownloaderHandler.__name__)
        ),
    )
    container.register(
        PDFCreatorHandler,
        lambda: PDFCreatorHandler(
            container.resolve_factory(LoggerProtocol, PDFCreatorHandler.__name__),
        ),
    )

    return container


def __env_service_factory():
    environService = EnvironConfig()
    if environService.get_config_value(ConfigEnum.E_MANGA_DOMAIN):
        return environService
    return ConfigParserService()
