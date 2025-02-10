from feature_interfaces.services.file_manager import IFileManager
from os import path, makedirs, listdir, remove
from shutil import rmtree, move, Error
from configs.my_logger import get_logger

DOWNLOAD_FOLDER = path.normpath(
            path.expanduser("~/Desktop")) + "/Manga_downloads"

class FileManager(IFileManager):
    IMAGE_TYPES= ["PNG","JPG", "JPEG", "WEBP", "GIF"]

    def __init__(self, rootPath:str, folderName:str | None):
        folder = "." if folder is None else folder
        rawFullPath = path.join(rootPath, folderName)
        directory, folder = path.split(rawFullPath)
        if folder == "..":
            directory, folder = path.split(directory)
            rawFullPath = directory
            directory, folder = path.split(directory)

        self.RootPath = directory
        self.FolderName = folder
        self.FullPath = rawFullPath

        self._logger = get_logger(__name__)
        if not path.exists(self.FullPath):
            makedirs(self.FullPath)

    def GetFolderPath(self):
        return self.FullPath

    def GetRootPath(self):
        return self.RootPath

    def HasFile(self, fileName: str) -> bool:
        return path.exists(self.GetFilePath(fileName))

    def GetFilePath(self, fileName: str) -> str:
        return path.join(self.FullPath, fileName)

    def GetImagesInFolder(self) -> list[str]:
        elementos = listdir(self.FullPath)
        return [ele for ele in elementos\
            if ele.split(".")[-1].upper() in FileManager.IMAGE_TYPES
        ]

    def MoveFileTo(self, fileName: str, destinyFolder: IFileManager):
        imagePath = self.GetFilePath(fileName)
        toMovePath = destinyFolder.GetFilePath(fileName)
        try:
            if path.exists(toMovePath):
                self._logger.info("Duplicated file [%s]", fileName)
                return
            move(imagePath, toMovePath)
        except Error as e:
            self ._logger.error("Error al copiar el archivo: %r",e)

    def DeleteAll(self, fromRootFolder: bool):
        if not path.exists(self.FullPath):
            return
        if not fromRootFolder:
            rmtree(self.FullPath)
        else:
            rmtree(self.RootPath)

    def DeleteFile(self, file: str):
        fileFullPath = self.GetFilePath(file)
        if not path.exists(fileFullPath):
            return
        remove(fileFullPath)
