from feature_interfaces.services.error_handler import IErrorHandler
from feature_interfaces.services.file_manager import IFileScrapperManager
from io import SEEK_END
import configs.dependency_injection as IOT 

class ErrorHandler(IErrorHandler):
    def __init__(self, urlItem:str, filemanager: IFileScrapperManager):
        self._url = urlItem
        self._folderpath = filemanager.GetFolderPath()
        self._folderManager = filemanager
        self._generalErrorFolderManager = IOT.GetFileScrapperManager("~", "errors")
        self._errors = []

    def SaveDownloadError(self, message: str, item: int, totalItems:int, ex: Exception):
        if len(self._errors) == 0:
            self._WriteTextOnFile("errors.txt",[f"{self._url} | {self._folderpath}"])
        self._errors.append(message)

        self._WriteTextOnFile("errors.txt",[ f"Error in {item}"])

    def SaveMessageError(self, message: str, ex: Exception):
        del ex
        self._WriteTextOnFile("errors.txt",[f"{self._url} | {self._folderpath}",
                                             message])
        self._errors.append("Error getting data")

    def _WriteTextOnFile(self, file_name: str, lines:list[str]):
        filePath = self._folderManager.GetFilePath(file_name)
        with open(filePath, "a", encoding="utf-8") as file:
            file.seek(0, SEEK_END)
            for line in lines:
                file.writelines(line + "\n")

        generalFile = self._generalErrorFolderManager.GetFilePath("error.txt")
        with open(generalFile, "a", encoding="utf-8") as gFile:
            gFile.seek(0, SEEK_END)
            for line in lines:
                gFile.writelines(line + "\n")
