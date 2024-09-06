'''Service to save images'''

import urllib.request as request
import os

import infrastructure.my_logger as my_logger

class FileDownloader:
  '''Class to save images from http uri'''
  def __init__(self, folder):
    self.__folder = folder
    self.__logger = my_logger.GetLogger(__name__)

  def create_folder_if_not_exist(self):
    if not os.path.exists(self.__folder):
      self.__logger.debug("Creating [%s]", self.__folder)
      os.makedirs(self.__folder)
      return
    self.__logger.debug("Folder [%s] exist", self.__folder)

  def download_image(self, url, image_name):
    path = f'{self.__folder}/{image_name}'
    if os.path.exists(path):
      self.__logger.info("Duplicated image [%s]", image_name)
      return

    request.urlretrieve(url, path)
    self.__logger.info("Get image [%s]", image_name)
