'''Strategi context'''
from exceptions.http_service_exception import HttpServiceException
from feature.manga_strategy.manga_interfaces import IMangaStrategy
from infrastructure.file_manager import FileDownloader
import configs.my_logger as MyLogger

class MangaScraper:
  '''process to download mangas'''
  def __init__(
      self, 
      strategy: IMangaStrategy
  ) -> None:
    self.strategy = strategy
    self._logger = MyLogger.get_logger(__name__)

  def run_manga_download_async(
      self, folder: FileDownloader,
      manga_page:int = 0, index_page: int = 0) -> list:
    del index_page
    errors = []
    current_page = self.strategy.get_first_page(manga_page)

    while True:
      try:
        (image_url, headers) = current_page.get_img_url()
        (image_number, last_number) = current_page.get_image_number()
        image_name = f"{image_number}_{current_page.get_image_name()}"

        self._logger.info("Trying to get page [%s: %s-%s]",
                           image_name, image_number, last_number)
        folder.get_image_from_url(image_url, image_name, headers)

      except HttpServiceException as ex:
        errors.append(current_page.get_image_name())
        self._logger.error(
          "Page: %s, Error= %r",
          current_page.get_image_number(), ex, exc_info=True)

      if current_page.is_last_page():
        break
      current_page = current_page.get_next_page_async()

    self._logger.info(
      "Download of [%s] complete", current_page.get_manga_name())
    return errors
