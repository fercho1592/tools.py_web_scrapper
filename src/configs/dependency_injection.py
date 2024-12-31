from feature_interfaces.services.error_handler import IErrorHandler
from feature.manga_strategy.manga_interfaces import IMangaStrategy

from feature.services.error_handler import ErrorHandler
from feature.services.user_feedback_handler import UserFeedbackHandler
from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature.services.file_manager import FileManager

def GetErrorHandler(mangaUrl: str, folderName: str):
    return ErrorHandler(mangaUrl, folderName)

def GetUserFeddbackHandler(folderName:str, errorHandler: IErrorHandler):
    return UserFeedbackHandler(folderName, errorHandler)

def GetMangaScrapper(strategy: IMangaStrategy):
    return MangaScraper(strategy)

def GetFileManager(rootPath, folder):
    return FileManager(rootPath, folder)
