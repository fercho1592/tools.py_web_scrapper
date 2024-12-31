'''Strategi context'''
from exceptions.http_service_exception import HttpServiceException
from feature.manga_strategy.manga_interfaces import IMangaStrategy,IMangaIndex
from feature_interfaces.services.file_manager import IFileManager
import configs.my_logger as MyLogger
from tools.string_path_fix import FixStringsTools
from tqdm import tqdm

class MangaScraper:
    '''process to download mangas'''
    def __init__(
        self,
        strategy: IMangaStrategy
    ) -> None:
        self.Strategy = strategy
        self._logger = MyLogger.get_logger(__name__)

    def run_manga_download_async(
        self,
        folder: IFileManager,
        manga_page:int = 0
    ) -> list:
        errors = []
        try:
            current_page = self.Strategy.get_first_page(manga_page)
            (image_number, last_number) = current_page.get_image_number()
            int_last_number = int(last_number)
            strategy_url = self.Strategy.get_url()
            print(f"Start download of {strategy_url} in [{folder.folder_path}]")
            progress_bar = tqdm(range(int_last_number), "Downloading images", int_last_number)
            progress_bar.update(manga_page)
        except Exception as ex:
            del ex
            folder.write_file("errors.txt",[f"{self.Strategy.get_url()} | {folder.folder_path}",
                                             "Erron getting data"])
            errors.append("Error getting data")
            return errors

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
                if len(errors) == 0:
                    folder.write_file("errors.txt",[f"{strategy_url} | {folder.folder_path}"])
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
        index:IMangaIndex = self.Strategy.get_index_page(self.Strategy.get_url())
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
