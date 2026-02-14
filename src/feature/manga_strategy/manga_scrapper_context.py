from feature.services.file_manager import FileManager
from feature.services.user_feedback_handler import ProgressBar
from feature_interfaces.models.folders_struct import FolderPath
from feature_interfaces.services.http_service import IHttpService
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from tools.string_path_fix import FixStringsTools


class MangaScraper:
    def __init__(
        self,
        strategy: IMangaStrategy,
        logger: LoggerProtocol,
        httpService: IHttpService,
    ) -> None:
        self.Strategy = strategy
        self._logger = logger
        self._httpService = httpService

    def set_starting_page(self, page_number: int = 0) -> None:
        try:
            self.currentPage = self.Strategy.get_first_page(page_number)
            (imageNumber, lastNumber) = self.currentPage.get_image_number()
            intLastNumber = int(lastNumber)

            self.progressBar = ProgressBar(intLastNumber, "")
            self.progressBar.SetCurrentProcess(page_number)
        except Exception as ex:
            self._logger.error("Error getting data from [%s]", self.Strategy.get_url())
            raise Exception("Error getting manga data") from ex

    def download_current_page(self, folderPath: FolderPath) -> None:
        fileManager = FileManager(self._logger)
        fileManager.CreateIfNotexist(folderPath)

        try:
            (imageUrl, headers) = self.currentPage.get_img_url()
            (imageNumber, lastNumber) = self.currentPage.get_image_number()
            imageName = self.currentPage.get_image_name()

            self._logger.info(
                "Trying to get page [%s: %s-%s]", imageName, imageNumber, lastNumber
            )

            if fileManager.HasFile(folderPath, imageName):
                self._logger.info("File already exists: [%s]", imageName)
                return

            self._httpService.SetHeaders(headers)
            self._httpService.DownloadImageFromUrl(
                imageUrl, imageName, folderPath.full_path
            )
        except Exception as ex:
            self._logger.error("Error downloading image from [%s]", imageUrl)
            raise Exception("Error downloading image") from ex

    def set_next_page(self) -> bool:
        try:
            self.progressBar.NextItem()
            if self.currentPage.is_last_page():
                return False
            self.currentPage = self.currentPage.get_next_page_async()
            return True
        except Exception as ex:
            self._logger.error(
                "Error getting next page from [%s]", self.Strategy.get_url()
            )
            raise Exception("Error getting next page") from ex

    def get_current_page(self):
        (imageNumber, lastNumber) = self.currentPage.get_image_number()
        return (imageNumber, lastNumber)

    def get_manga_data(self) -> dict[str, str]:
        index = self.Strategy.get_index_page(self.Strategy.get_url())
        name = FixStringsTools.FixStringForPath(index.get_manga_name())
        artist = " | ".join(index.get_manga_artist())
        groups = " | ".join(index.get_manga_group())
        genders = " | ".join(index.get_manga_genders())
        (_, last_page) = self.get_current_page()

        return {
            "name": name,
            "artist": artist,
            "groups": groups,
            "genders": genders,
            "last_page": last_page
        }
