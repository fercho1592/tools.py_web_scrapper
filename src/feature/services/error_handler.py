from feature_interfaces.services.error_handler import IErrorHandler
from io import SEEK_END
from os import path

class ErrorLogFileHandler(IErrorHandler):
    FILE_NAME = "errors.txt"
    GLOBAL_ERROR_LOG_FOLDER = "./errors"
    
    def __init__(self, urlItem:str, folder_path:str):
        self._url = urlItem
        self._folderpath = folder_path
        self._errors = []

    def SaveDownloadError(self, message: str, item: int, totalItems:int, ex: Exception):
        if len(self._errors) == 0:
            self._WriteTextOnFile(ErrorLogFileHandler.FILE_NAME,[f"{self._url} | {self._folderpath}"])
        self._errors.append(message)

        self._WriteTextOnFile(ErrorLogFileHandler.FILE_NAME,[ f"Error in {item}"])

    def SaveMessageError(self, message: str, ex: Exception):
        del ex
        self._WriteTextOnFile(ErrorLogFileHandler.FILE_NAME,[f"{self._url} | {self._folderpath}",
                                             message])
        self._errors.append("Error getting data")

    def _WriteTextOnFile(self, file_name: str, lines:list[str]):
        filePath = path.join(self._folderpath, file_name)
        with open(filePath, "a", encoding="utf-8") as file:
            file.seek(0, SEEK_END)
            for line in lines:
                file.writelines(line + "\n")

        with open(f"{ErrorLogFileHandler.GLOBAL_ERROR_LOG_FOLDER}/{ErrorLogFileHandler.FILE_NAME}", "a", encoding="utf-8") as gFile:
            gFile.seek(0, SEEK_END)
            for line in lines:
                gFile.writelines(line + "\n")
