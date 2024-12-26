from feature_interfaces.services.error_handler import IErrorHandler
from infrastructure.file_manager import FileManager
from logging import Logger
from io import SEEK_END
from enum import Enum

class ErrorHandler(IErrorHandler):
    def __init__(self, urlItem:str, folderPath:str, logger: Logger):
        self._url = urlItem
        self._folderpath = folderPath
        self._folderManager = FileManager(folderPath)
        self._errors = []
        self._logger = logger

    def SaveDownloadError(self, message: str, item: int, totalItems:int, ex: Exception):
        if len(self._errors) == 0:
            self._WriteTextOnFile("errors.txt",[f"{self._url} | {self._folderpath}"])
        self._errors.append(item)

        self._WriteTextOnFile("errors.txt",[ f"Error in {item}"])
        self._logger.error("Page: %s, Error= %r",item, ex, exc_info=True)
    
    def SaveMessageError(self, message: str, ex: Exception):
        self._WriteTextOnFile("errors.txt",[f"{self._url} | {self._folderpath}",
                                             "Erron getting data"])
        self._errors.append("Error getting data")

    def _WriteTextOnFile(self, file_name: str, lines:list[str]):
        with open(f"{self._folderManager.folder_path}/{file_name}", "a", encoding="utf-8") as file:
            file.seek(0, SEEK_END)
            for line in lines:
                file.writelines(line + "\n")