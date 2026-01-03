from feature_interfaces.services.http_service import IHttpService
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy
from feature_interfaces.services.file_manager import IFileScrapperManager
from feature_interfaces.services.user_feedback_handler import IUserFeedbackHandler
from tools.string_path_fix import FixStringsTools
from feature_interfaces.protocols.config_protocol import LoggerProtocol


class MangaScraper:
    def __init__(self,
                strategy: IMangaStrategy,
                fileManager: IFileScrapperManager,
                uiHandler: IUserFeedbackHandler,
                logger: LoggerProtocol,
                httpService: IHttpService
                ) -> None:
        self.Strategy = strategy
        self.FileManager = fileManager
        self._uiHandler = uiHandler
        self._logger = logger
        self._httpService = httpService

    def run_manga_download_async(self, manga_page:int = 0) -> None:
        try:
            currentPage = self.Strategy.get_first_page(manga_page)
            (imageNumber, lastNumber) = currentPage.get_image_number()
            intLastNumber = int(lastNumber)
            strategyUrl = self.Strategy.get_url()

            self._uiHandler.ShowMessage(
                f"Start download of {strategyUrl} in [{self.FileManager.GetFolderPath()}]")
            progressBar = self._uiHandler.CreateProgressBar(intLastNumber, "")
            progressBar.SetCurrentProcess(manga_page)
        except Exception as ex:
            self._uiHandler.ShowMessageError("Error getting data", ex)
            raise ex

        while True:
            try:
                (imageUrl, headers) = currentPage.get_img_url()
                (imageNumber, lastNumber) = currentPage.get_image_number()
                imageName = currentPage.get_image_name()

                self._logger.info(
                    "Trying to get page [%s: %s-%s]",imageName, imageNumber, lastNumber)

                if not self.FileManager.HasFile(imageName):
                    self._httpService.SetHeaders(headers)
                    self._httpService.DownloadImageFromUrl(
                        imageUrl, imageName, self.FileManager.GetFolderPath())
                progressBar.NextItem()
            except Exception as ex:
                self._uiHandler.ShowMessageError(f"Error in {currentPage.get_image_number()}", ex)
                raise ex
            if currentPage.is_last_page():
                break
            currentPage = currentPage.get_next_page_async()

        self._logger.info("Download of [%s] complete", currentPage.get_manga_name())
        self._uiHandler.ShowMessage(f"Download of {currentPage.get_manga_name()} complete")
        
    def get_manga_data(self) -> dict[str,str]:
        index = self.Strategy.get_index_page(self.Strategy.get_url())
        name = FixStringsTools.FixStringForPath(index.get_manga_name())
        artist =  " | ".join(index.get_manga_artist())
        groups = " | ".join(index.get_manga_group())
        genders = " | ".join(index.get_manga_genders())

        return {
            "name": name,
            "artist": artist,
            "groups": groups,
            "genders": genders,
        }
