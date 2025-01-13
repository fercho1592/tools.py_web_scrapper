from feature_interfaces.services.error_handler import IErrorHandler
from feature_interfaces.services.user_feedback_handler import IUserFeedbackHandler
from feature_interfaces.services.file_manager import IFileManager
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy

from feature.services.error_handler import ErrorHandler
from feature.services.user_feedback_handler import UserFeedbackHandler
from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature.services.file_manager import FileManager
from feature.image_converter.pillow_image_converter import PillowImageConverter
from feature.manga_strategy.manga_factory import MangaFactory
from infrastructure.http_service import HttpService

def GetErrorHandler(mangaUrl: str, fileManager: IFileManager):
    return ErrorHandler(mangaUrl, fileManager)

def GetFileManager(rootPath, folder):
    return FileManager(rootPath, folder)

def GetMangaStrategy(url: str):
    return MangaFactory.get_manga_strategy(url)

def GetUserFeddbackHandler(folderName:str, errorHandler: IErrorHandler):
    return UserFeedbackHandler(folderName, errorHandler)

def GetMangaScrapper(
        strategy: IMangaStrategy, uiHandler: IUserFeedbackHandler, fileManager: IFileManager):
    return MangaScraper(strategy, fileManager, uiHandler)

def GetImageConverter():
    return PillowImageConverter()

def GetHttpService():
    return HttpService()
