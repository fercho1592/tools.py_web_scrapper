'''Strategi context'''
from manga_interfaces import IMangaStrategy
from infrastructure.file_downloader import FileDownloader
import infrastructure.my_logger as MyLogger
__logger = MyLogger.get_logger(__name__)

class MangaScraper:
  '''process to download mangas'''
  def __init__(self, strategy: IMangaStrategy) -> None:
    self.strategy = strategy

  def run_manga_download_async(
      self, folder: FileDownloader, manga_page:int = 0, index_page: int = 0):
    errors = []
    current_page = self.strategy.get_first_page(manga_page, index_page)

    while True:
      try:
        image_url = current_page.get_img_url()
        image_name = current_page.get_image_name()
        image_number = current_page.get_image_number()

        __logger.info("Trying to get page [%s: %s]", image_name, image_number)
        folder.downloadImage(image_url, image_name)
        if current_page.is_last_page():
          __logger.info(
            "Download of [%s] complete", current_page.get_manga_name())
          break
        current_page = current_page.get_next_page_async()
      except Exception as ex:
        errors.append(current_page.get_image_name())
        __logger.error(
          "Page: %s, Error= %r",
          current_page.get_image_number(), ex, exc_info=True)
        current_page = current_page.get_next_page_async()

    return errors
