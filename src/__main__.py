'''Main code'''
from infrastructure.file_downloader import FileDownloader
from infrastructure.file_manager import read_queue
from infrastructure.my_logger import get_logger
from feature.manga_strategy.manga_factory import MangaFactory
from feature.manga_strategy.manga_scrapper_context import MangaScraper

_logger = get_logger(__name__)

def main():
  download_queue = read_queue()

  error_list = {}

  for item in download_queue:
    print("*************************************************")
    strategy = MangaFactory.get_manga_strategy(item[0])
    scrapper = MangaScraper(strategy)

    folder_manager = FileDownloader(f"../{item[1]}")
    folder_manager.create_folder_if_not_exist()

    _logger.info("Start manga download for [%s]", item[1])
    error_by_manga = scrapper.run_manga_download_async(folder_manager, item[2])

    error_list[item[1]] = error_by_manga

    if len(error_by_manga) > 0:
      print(f"Error in these images from [{item[0]}]", error_by_manga[1])

    _logger.info("End manga download for [%s]", item[1])

  print(error_list)


if __name__ == "__main__":
  main()
