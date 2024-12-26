from feature_interfaces.services.error_handler import IErrorHandler
from infrastructure.file_manager import FileDownloader
from logging import Logger
from abc import ABC

class ErrorHandler(IErrorHandler):
    def __init__(self, urlItem:str, folderPath:str, logger: Logger):
        self._url = urlItem
        self._folderpath = folderPath
        self._folderManager = FileDownloader(folderPath)
        self._errors = []
        self._logger = logger

    def SaveDownloadError(self, message: str, item: int, totalItems:int, ex: Exception):
        if len(self._errors) == 0:
            self._folderManager.write_file("errors.txt",[f"{self._url} | {self._folderpath}"])
        self._errors.append(item)

        self._folderManager.write_file("errors.txt",[ f"Error in {item}"])
        self._logger.error("Page: %s, Error= %r",item, ex, exc_info=True)
    
    def SaveMessageError(self, message: str, ex: Exception):
        self._folderManager.write_file("errors.txt",[f"{self._url} | {self._folderpath}",
                                             "Erron getting data"])
        self._errors.append("Error getting data")
