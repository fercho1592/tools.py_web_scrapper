from feature_interfaces.models.folders_struct import FolderPath
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from os import path, makedirs, listdir, remove
from shutil import rmtree, move, Error

DOWNLOAD_FOLDER = path.normpath(path.expanduser("~/Desktop"))


class FileManager:
    IMAGE_TYPES = ["PNG", "JPG", "JPEG", "WEBP", "GIF"]

    def __init__(self, logger: LoggerProtocol):
        self._logger = logger
        pass

    def CreateIfNotexist(self, folder_path: FolderPath):
        if not path.exists(folder_path.full_path):
            makedirs(folder_path.full_path)

    def HasFile(self, folder_path: FolderPath, file_name: str) -> bool:
        fileFullPath = folder_path.get_file_path(file_name)
        if not path.exists(fileFullPath):
            return False
        return True

    def GetImagesInFolder(self, folder_path: FolderPath) -> list[str]:
        elementos = listdir(folder_path.full_path)
        elementos.sort()
        return [
            ele
            for ele in elementos
            if ele.split(".")[-1].upper() in FileManager.IMAGE_TYPES
        ]

    def DeleteAll(self, fromRootFolder: FolderPath):
        if not path.exists(fromRootFolder.root_path):
            return
        else:
            rmtree(fromRootFolder.root_path)

    def DeleteFile(self, folder_path: FolderPath, file: str):
        fileFullPath = folder_path.get_file_path(file)
        if not path.exists(fileFullPath):
            return
        remove(fileFullPath)

    def MoveFileTo(
        self, sourceFolder: FolderPath, fileName: str, destinyFolder: FolderPath
    ):
        imagePath = sourceFolder.get_file_path(fileName)
        toMovePath = destinyFolder.get_file_path(fileName)
        try:
            if path.exists(toMovePath):
                self._logger.info("Duplicated file [%s]", fileName)
                return
            move(imagePath, toMovePath)
        except Error as e:
            self._logger.error("Error al copiar el archivo: %r", e)
