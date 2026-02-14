from dataclasses import dataclass
from feature_interfaces.models.folders_struct import FolderPath
from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature_interfaces.protocols.config_protocol import LoggerProtocol


@dataclass
class MangaDownloaderCommand:
    scrapper: MangaScraper
    pageNumber: int
    folderPath: FolderPath


class MangaDownloaderHandler:
    def __init__(self, loggerFactory: LoggerProtocol):
        self._logger = loggerFactory

        # requires scrapper

    async def handle(self, command: MangaDownloaderCommand):
        try:
            self._logger.info(
                "Start manga download for [%s]", command.folderPath.relative_path
            )

            command.scrapper.set_starting_page(command.pageNumber)
            while True:
                command.scrapper.download_current_page(command.folderPath)
                hasNext = command.scrapper.set_next_page()
                if not hasNext:
                    break
        except Exception as ex:
            (current_page, total_pages) = command.scrapper.get_current_page()
            raise Exception(
                f"Error during manga download in item [{current_page}/{total_pages}]"
            ) from ex
