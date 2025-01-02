from feature_interfaces.services.error_handler import IErrorHandler
from feature_interfaces.services.file_manager import IFileManager
from io import SEEK_END

class ErrorHandler(IErrorHandler):
    def __init__(self, urlItem:str, filemanager: IFileManager):
        self._url = urlItem
        self._folderpath = filemanager.GetFolderPath()
        self._folderManager = filemanager
        self._errors = []

    def SaveDownloadError(self, message: str, item: int, totalItems:int, ex: Exception):
        if len(self._errors) == 0:
            self._WriteTextOnFile("errors.txt",[f"{self._url} | {self._folderpath}"])
        self._errors.append(item)

        self._WriteTextOnFile("errors.txt",[ f"Error in {item}"])

    def SaveMessageError(self, message: str, ex: Exception):
        del ex
        self._WriteTextOnFile("errors.txt",[f"{self._url} | {self._folderpath}",
                                             "Erron getting data"])
        self._errors.append("Error getting data")

    def _WriteTextOnFile(self, file_name: str, lines:list[str]):
        with open(f"{self._folderManager.folder_path}/{file_name}", "a", encoding="utf-8") as file:
            file.seek(0, SEEK_END)
            for line in lines:
                file.writelines(line + "\n")
