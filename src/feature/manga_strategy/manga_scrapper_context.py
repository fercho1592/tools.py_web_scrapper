'''Strategi context'''
from feature.manga_strategy.manga_interfaces import IMangaStrategy
from infrastructure.file_downloader import FileDownloader
import infrastructure.my_logger as MyLogger

class MangaScraper:
  '''process to download mangas'''
  def __init__(self, strategy: IMangaStrategy) -> None:
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
        image_url = current_page.get_img_url()
        image_name = current_page.get_image_name()
        image_number = current_page.get_image_number()

        self._logger.info("Trying to get page [%s: %s]",
                           image_name, image_number)
        folder.download_image(image_url, image_name)
        if current_page.is_last_page():
          self._logger.info(
            "Download of [%s] complete", current_page.get_manga_name())
          break
        current_page = current_page.get_next_page_async()
      except Exception as ex:
        errors.append(current_page.get_image_name())
        self._logger.error(
          "Page: %s, Error= %r",
          current_page.get_image_number(), ex, exc_info=True)
        current_page = current_page.get_next_page_async()

    return errors
