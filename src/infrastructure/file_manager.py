'''Service to save images'''

import os
import infrastructure.http_service as http_service

import infrastructure.my_logger as my_logger

class FileDownloader:
  '''Class to save images from http uri'''
  def __init__(self, folder: str):
    self.folder_path = folder
    self.__logger = my_logger.get_logger(__name__)

  def create_folder_if_not_exist(self):
    if not os.path.exists(self. folder_path):
      self.__logger.debug("Creating [%s]", self. folder_path)
      os.makedirs(self. folder_path)
      return
    self.__logger.debug("Folder [%s] exist", self. folder_path)

  def get_image_from_url(self, url, image_name, headers):
    path = f'{self. folder_path}/{image_name}'
    if os.path.exists(path):
      self.__logger.info("Duplicated image [%s]", image_name)
      return

    http_service.download_image_from_url(url, path, headers)

    self.__logger.info("Get image [%s]", image_name)

  def get_images_in_folder(self) -> list[str]:
    elementos = os.listdir(self. folder_path)
    return elementos
