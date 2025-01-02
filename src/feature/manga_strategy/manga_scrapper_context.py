'''Strategi context'''
from exceptions.http_service_exception import HttpServiceException
from feature.manga_strategy.manga_interfaces import IMangaStrategy
from feature_interfaces.services.file_manager import IFileManager
from feature_interfaces.services.user_feedback_handler import IUserFeedbackHandler
from tools.string_path_fix import FixStringsTools
import configs.my_logger as MyLogger
import configs.dependency_injection as IOT

class MangaScraper:
    '''process to download mangas'''
    def __init__(self,strategy: IMangaStrategy,uiHandler: IUserFeedbackHandler) -> None:
        self.Strategy = strategy
        self._uiHandler = uiHandler
        self._logger = MyLogger.get_logger(__name__)
        self._httpService =  IOT.GetHttpService()

    def run_manga_download_async(self, folder: IFileManager, manga_page:int = 0) -> None:
        errors = []
        try:
            currentPage = self.Strategy.get_first_page(manga_page)
            (imageNumber, lastNumber) = currentPage.get_image_number()
            intLastNumber = int(lastNumber)
            strategyUrl = self.Strategy.get_url()

            self._uiHandler.ShowMessage(
                f"Start download of {strategyUrl} in [{folder.GetFolderPath()}]")
            progressBar = self._uiHandler.CreateProgressBar(intLastNumber, "")
            progressBar.SetCurrentProcess(manga_page)
        except Exception as ex:
            self._uiHandler.ShowMessageError("Error getting data", ex)

        while True:
            try:
                (imageUrl, headers) = currentPage.get_img_url()
                (imageNumber, lastNumber) = currentPage.get_image_number()
                imageName = currentPage.get_image_name()

                self._logger.info(
                    "Trying to get page [%s: %s-%s]",imageName, imageNumber, lastNumber)

                self._httpService.SetHeaders(headers)
                self._httpService.DownloadImageFromUrl(imageUrl, imageName, folder.GetFolderPath())
                progressBar.NextItem()
            except HttpServiceException as ex:
                self._uiHandler.ShowMessageError(f"Error in {currentPage.get_image_number()}", ex)

            if currentPage.is_last_page():
                break
            currentPage = currentPage.get_next_page_async()

        self._logger.info("Download of [%s] complete", currentPage.get_manga_name())
        return errors

    def get_manga_data(self) -> dict[str,str]:
        index = self.Strategy.get_index_page(self.Strategy.get_url())
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
