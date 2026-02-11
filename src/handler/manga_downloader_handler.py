from dataclasses import dataclass
from configs.logger_factory import LoggerFactory
from feature_interfaces.models.folders_struct import FolderPath
from feature_interfaces.protocols.factory_protocol import MangaFactoryProtocol
from feature.manga_strategy.manga_scrapper_context import MangaScraper


@dataclass
class MangaDownloaderCommand:
    scrapper: MangaScraper
    pageNumber: int
    folderPath: FolderPath


class MangaDownloaderHandler:
    def __init__(self, loggerFactory: LoggerFactory, factory: MangaFactoryProtocol):
        self._factory = factory
        self._logger = loggerFactory.get_logger(__name__)

        # requires scrapper

    async def handler(self, command: MangaDownloaderCommand):
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
