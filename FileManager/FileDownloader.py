import urllib.request as request
import os

import MyLogger


class FileDownloader:
    def __init__(self, folder):
        self.__folder = folder
        self.__logger = MyLogger.GetLogger(__name__)

    def createFolderIfNotExist(self):
        if not os.path.exists(self.__folder):
            self.__logger.debug(f"Creating [{self.__folder}]")
            os.makedirs(self.__folder)
            return
        self.__logger.debug(f"Folder [{self.__folder}] exist")
        

    def downloadImage(self, url, imageName):
        path = f'{self.__folder}/{imageName}'
        if os.path.exists(path):
            self.__logger.info(f"Duplicated image [{imageName}]")
            return

        request.urlretrieve(url, path)
        self.__logger.info(f"Get image [{imageName}]")