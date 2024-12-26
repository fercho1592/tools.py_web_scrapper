'''Service to save images'''
import os
import shutil
import infrastructure.http_service as http_service

import configs.my_logger as my_logger

class FileManager:
    '''Class to save images from http uri'''
    def __init__(self, folder: str):
        self.folder_path = folder
        self.__logger = my_logger.get_logger(__name__)

    def create_folder_if_not_exist(self, folder_path = None):
        folder_path = self.folder_path if folder_path is None else folder_path
        if not os.path.exists(folder_path):
            self.__logger.debug("Creating [%s]", folder_path)
            os.makedirs(folder_path)
            return
        self.__logger.debug("Folder [%s] exist", folder_path)
        return

    def exist_file(self, file_path):
        return os.path.exists(file_path)

    def get_image_from_url(self, url, image_name, headers):
        path = f'{self. folder_path}/{image_name}'
        if os.path.exists(path):
            self.__logger.info("Duplicated image [%s]", image_name)
            return

        http_service.download_image_from_url(url, path, headers)

        self.__logger.info("Get image [%s]", image_name)

    def get_images_in_folder(self) -> list[str]:
        elementos = os.listdir(self.folder_path)
        return [ele for ele in elementos\
            if ele.split(".")[-1].upper() in ["PNG","JPG", "JPEG", "WEBP"]
        ]

    def copy_image_to(self, file, folder):
        image_full_path = f"{self.folder_path}/{file}"
        folder_full_path = folder
        try:
            self.create_folder_if_not_exist(folder_full_path)
            if os.path.exists(f"{folder_full_path}/{file}"):
                self.__logger.info("Duplicated file [%s]", file)
                return
            shutil.copy2(image_full_path, folder_full_path)
        except shutil.Error as e:
            self .__logger.error("Error al copiar el archivo: %r",e)

    def delete_all(self):
        shutil.rmtree(self.folder_path)
