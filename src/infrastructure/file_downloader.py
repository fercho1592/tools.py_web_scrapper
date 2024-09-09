'''Service to save images'''

import os
import infrastructure.http_service as http_service

import infrastructure.my_logger as my_logger

class FileDownloader:
  '''Class to save images from http uri'''
  def __init__(self, folder: str):
    self._folder = folder
    self.__logger = my_logger.get_logger(__name__)

  def create_folder_if_not_exist(self):
    if not os.path.exists(self._folder):
      self.__logger.debug("Creating [%s]", self._folder)
      os.makedirs(self._folder)
      return
    self.__logger.debug("Folder [%s] exist", self._folder)

  def download_image(self, url, image_name):
    path = f'{self._folder}/{image_name}'
    if os.path.exists(path):
      self.__logger.info("Duplicated image [%s]", image_name)
      return

    http_service.download_image_from_url(url, path)

    self.__logger.info("Get image [%s]", image_name)
