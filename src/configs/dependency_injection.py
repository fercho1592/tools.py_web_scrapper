from functools import partial
from feature.services.file_manager import FileManager
from feature_interfaces.enums.settings_enum import ConfigEnum, FunctionEnum
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

import handler.image_converter_handler as image_converter_handler
import handler.manga_downloader_handler as manga_downloader_handler
import handler.pdf_creator_handler as pdf_creator_handler
import handler.webdav_handler as webdav_handler

from infrastructure.http_service import HttpService
from infrastructure.pdf_generator import PdfCreator
from configs.config_manager import ConfigParserService, EnvironConfig
from configs.logger_factory import LoggerFactory


def build_container():
    container = Container()
    build_factories(container)
    build_partials(container)
    return container


def build_factories(container: Container):
    container.register(
        IHttpService,
        lambda: HttpService(
            container.resolve_factory(LoggerProtocol, HttpService.__name__)
        ),
    )
    container.register(ConfigServiceProtocol, _env_service_factory, is_singleton=True)
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


def _env_service_factory():
    environService = EnvironConfig()
    if environService.get_config_value(ConfigEnum.E_MANGA_DOMAIN):
        return environService
    return ConfigParserService()


def build_partials(container: Container):
    fn_pdf_handler = partial(
        pdf_creator_handler.handle, pdf_creator_service=container.resolve(IPdfCreator)
    )

    logger = container.resolve_factory(LoggerProtocol, webdav_handler.__name__)
    fn_webdav_handler = partial(
        webdav_handler.handle,
        webdav_service=container.resolve(WebDAVService),
        FileManager=FileManager(logger),
        logger=logger,
    )

    fn_manga_downloader_handler = partial(
        manga_downloader_handler.handle,
        logger=container.resolve_factory(
            LoggerProtocol, manga_downloader_handler.__name__
        ),
    )
    fn_image_converter_handler = partial(
        image_converter_handler.handle,
        image_editor_service=container.resolve(IImageEditorService),
        logger=container.resolve_factory(
            LoggerProtocol, image_converter_handler.__name__
        ),
    )

    container.register_function(FunctionEnum.PDF_CREATOR, fn_pdf_handler)
    container.register_function(FunctionEnum.WEBDAV, fn_webdav_handler)
    container.register_function(
        FunctionEnum.MANGA_DOWNLOADER, fn_manga_downloader_handler
    )
    container.register_function(
        FunctionEnum.IMAGE_CONVERTER, fn_image_converter_handler
    )
