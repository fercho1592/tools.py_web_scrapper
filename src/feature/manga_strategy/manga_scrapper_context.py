'''Strategi context'''

from WebReaders.e_web_reader import EWebScraper
from infrastructure.file_downloader import FileDownloader
import infrastructure.my_logger as MyLogger
__logger = MyLogger.get_logger(__name__)

def GetMangaFromIndex(url, manga_name, page= 1):
  __logger.info("Start getting manga from index [%s]", manga_name)
  folder = FileDownloader(manga_name)
  folder.create_folder_if_not_exist()

  web_scrapper = EWebScraper(url)
  index = web_scrapper.getIndexPageAsync()
  page_count = index.getMangaPageCount()
  __logger.info("Manga [%s] contains %s", manga_name, page_count)
  page_html_component = index.getMangaPageAsync(page)
  errors = RunMangaDownloaderAsync(page_html_component, folder, manga_name)
  return (manga_name, errors)

def GetMangaFromPage(url, manga_name):
  __logger.info("Start getting manga from page [%s]", manga_name)
  folder = FileDownloader(manga_name)
  folder.create_folder_if_not_exist()

  web_scrapper = EWebScraper(url)
  page_html_component = web_scrapper.getPageAsync()
  errors = RunMangaDownloaderAsync(page_html_component, folder, manga_name)
  return (manga_name, errors)

def RunMangaDownloaderAsync(page_html_component, folder, manga_name):
  errors = []
  current_page = page_html_component
  while True:
    try:
      image_url = current_page.GetImgUrl()
      image_name = current_page.getImageName()
      image_number = current_page.getImageNumber()

      __logger.info("Trying to get page [%s: %s]", image_name, image_number)
      folder.downloadImage(image_url, image_name)
      if current_page.isLastPage():
        __logger.info("Download of [%s] complete", manga_name)
        break
      current_page = current_page.get()
    except Exception as ex:
      errors.append(current_page.getImageNumber())
      __logger.error(
        "Page: %s, Error= %r", current_page.getImageNumber(), ex, exc_info=True)
      current_page = current_page.GetNextPageAsync()

    return errors

