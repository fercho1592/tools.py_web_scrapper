from feature.services.file_manager import FileManager
from feature_interfaces.models.folders_struct import FolderPath, WORKING_FOLDER
from feature_interfaces.services.error_handler import IErrorHandler
from io import SEEK_END
from os import path


class ErrorLogFileHandler(IErrorHandler):

    FILE_NAME = "errors.txt"
    GLOBAL_ERROR_LOG_FOLDER = FolderPath(WORKING_FOLDER, "./errors")

    def __init__(self, urlItem: str, folder_path: FolderPath):
        self._url = urlItem
        self._folderpath = folder_path
        self._errors = []

    def SaveDownloadError(self, message: str, ex: Exception):
        if len(self._errors) == 0:
            self._WriteTextOnFile(
                ErrorLogFileHandler.FILE_NAME,
                [f"{self._url} | {self._folderpath.relative_path}"],
            )
        self._errors.append(message)

    def SaveMessageError(self, message: str, ex: Exception):
        del ex
        self._WriteTextOnFile(
            ErrorLogFileHandler.FILE_NAME,
            [f"{self._url} | {self._folderpath.relative_path}", message],
        )
        self._errors.append("Error getting data")

    def _WriteTextOnFile(self, file_name: str, lines: list[str]):
        fileManager = FileManager(None)
        fileManager.CreateIfNotexist(self._folderpath)
        fileManager.CreateIfNotexist(ErrorLogFileHandler.GLOBAL_ERROR_LOG_FOLDER)
        filePath = path.join(self._folderpath.full_path, file_name)
        with open(filePath, "a", encoding="utf-8") as file:
            file.seek(0, SEEK_END)
            for line in lines:
                file.writelines(line + "\n")

        global_file_path = path.join(
            ErrorLogFileHandler.GLOBAL_ERROR_LOG_FOLDER.full_path,
            ErrorLogFileHandler.FILE_NAME,
        )
        with open(global_file_path, "a", encoding="utf-8") as gFile:
            gFile.seek(0, SEEK_END)
            for line in lines:
                gFile.writelines(line + "\n")
