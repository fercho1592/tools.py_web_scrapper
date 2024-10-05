'''Strategi context'''
from exceptions.http_service_exception import HttpServiceException
from feature.manga_strategy.manga_interfaces import IMangaStrategy,IMangaIndex
from infrastructure.file_manager import FileDownloader
import configs.my_logger as MyLogger
from tools.string_path_fix import FixStringsTools
from tqdm import tqdm

class MangaScraper:
    '''process to download mangas'''
    def __init__(
        self,
        strategy: IMangaStrategy
    ) -> None:
        self.strategy = strategy
        self._logger = MyLogger.get_logger(__name__)

    def run_manga_download_async(
        self,
        folder: FileDownloader,
        manga_page:int = 0,
        index_page: int = 0
    ) -> list:
        del index_page
        errors = []
        current_page = self.strategy.get_first_page(manga_page)
        (image_number, last_number) = current_page.get_image_number()
        int_last_number = int(last_number)
        print(f"Start download of {self.strategy.get_url()} in [{folder.folder_path}]")
        progress_bar = tqdm(range(int_last_number), "Downloading images", int_last_number)

        while True:
            try:
                (image_url, headers) = current_page.get_img_url()
                (image_number, last_number) = current_page.get_image_number()
                image_name = current_page.get_image_name()

                self._logger.info("Trying to get page [%s: %s-%s]",
                                    image_name, image_number, last_number)
                folder.get_image_from_url(image_url, image_name, headers)
                progress_bar.update()

            except HttpServiceException as ex:
                errors.append(current_page.get_image_name())

                folder.write_file("errors.txt",[
                    f"Error in {current_page.get_image_number()}"
                ])
                self._logger.error(
                    "Page: %s, Error= %r",
                    current_page.get_image_number(), ex, exc_info=True)

            if current_page.is_last_page():
                break
            current_page = current_page.get_next_page_async()

        self._logger.info(
            "Download of [%s] complete", current_page.get_manga_name())
        return errors

    def get_manga_data(self) -> dict[str,str]:
        index:IMangaIndex = self.strategy.get_index_page(self.strategy.get_url())
        name = FixStringsTools.fix_string_for_path(index.get_manga_name())
        artist =  " | ".join(index.get_manga_artist())
        groups = " | ".join(index.get_manga_group())
        genders = " | ".join(index.get_manga_genders())

        return {
            "name": name,
            "artist": artist,
            "groups": groups,
            "genders": genders,
        }
