from feature_interfaces.services.file_manager import IFileManager
from os import path, makedirs, listdir
from shutil import rmtree, move, Error
from configs.my_logger import get_logger

DOWNLOAD_FOLDER = path.normpath(
            path.expanduser("~/Desktop")) + "/Manga_downloads"

class FileManager(IFileManager):
    IMAGE_TYPES= ["PNG","JPG", "JPEG", "WEBP"]

    def __init__(self, rootPath:str, folderName:str):
        self.RootPath = rootPath
        self.FolderName = folderName
        self._logger = get_logger(__name__)

        self.FullPath = path.join(rootPath, folderName)
        if not path.exists(self.FullPath):
            makedirs(self.FullPath)

    def GetFolderPath(self):
        return self.FullPath

    def GetRootPath(self):
        return self.RootPath

    def HasFile(self, fileName: str) -> bool:
        return path.exists(path.join(self.FullPath, fileName))

    def GetImagesInFolder(self) -> list[str]:
        elementos = listdir(self.FullPath)
        return [ele for ele in elementos\
            if ele.split(".")[-1].upper() in FileManager.IMAGE_TYPES
        ]

    def MoveFileTo(self, fileName: str, destinyFolder: IFileManager):
        imagePath = f"{self.FullPath}/{fileName}"
        folderPath = destinyFolder.GetFolderPath()
        try:
            if path.exists(path.join(folderPath, fileName)):
                self._logger.info("Duplicated file [%s]", fileName)
                return
            move(imagePath, folderPath)
        except Error as e:
            self ._logger.error("Error al copiar el archivo: %r",e)

    def DeleteAll(self):
        rmtree(self.FullPath)
