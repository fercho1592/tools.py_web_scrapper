from feature_interfaces.services.error_handler import IErrorHandler
from feature_interfaces.services.user_feedback_handler import IUserFeedbackHandler
from feature_interfaces.services.file_manager import IFileScrapperManager
from feature_interfaces.services.http_service import IHttpService
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy
from feature_interfaces.web_drivers.i_web_reader_driver import IWebReaderDriver

from feature.services.error_handler import ErrorHandler
from feature.services.user_feedback_handler import UserFeedbackHandler
from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature.services.file_manager import FileManager
from feature.image_converter.pillow_image_converter import PillowImageConverter
from feature.manga_strategy.manga_factory import MangaFactory
from feature.web_driver.html_parser.html_decoder import HtmlDecoder
from feature.image_converter.image_converter_interfaces import IImageEditorService
from infrastructure.http_service import HttpService


def GetErrorHandler(mangaUrl: str, fileManager: IFileScrapperManager) -> IErrorHandler:
    return ErrorHandler(mangaUrl, fileManager)

def GetFileScrapperManager(rootPath: str, folder: str | None) -> IFileScrapperManager:
    return FileManager(rootPath, folder)

def GetMangaStrategy(url: str) -> IMangaStrategy:
    return MangaFactory.get_manga_strategy(url)

def GetUserFeddbackHandler(folderName:str, errorHandler: IErrorHandler) -> IUserFeedbackHandler:
    return UserFeedbackHandler(folderName, errorHandler)

def GetMangaScrapper(
        strategy: IMangaStrategy, uiHandler: IUserFeedbackHandler, fileManager: IFileScrapperManager):
    return MangaScraper(strategy, fileManager, uiHandler)

def GetImageConverter() -> IImageEditorService:
    return PillowImageConverter()

def GetHttpService() -> IHttpService:
    return HttpService()

def GetWebReaderDriver(url:str) -> IWebReaderDriver:
    httpService = GetHttpService()
    html = httpService.GetHtmlFromUrl(url)

    decoder = HtmlDecoder()
    decoder.set_html(html)

    return decoder.get_dom_component()