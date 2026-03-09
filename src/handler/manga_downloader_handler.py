from dataclasses import dataclass
from feature_interfaces.models.folders_struct import FolderPath
from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from wrappers.handler_decorators import log_ejecucion


@dataclass
class MangaDownloaderCommand:
    scrapper: MangaScraper
    pageNumber: int
    folderPath: FolderPath


@DeprecationWarning(
    "Use the handle function instead of the class-based handler for better performance and simplicity."
)
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


@log_ejecucion
async def handle(logger: LoggerProtocol, command: MangaDownloaderCommand):
    logger.info("Start manga download for [%s]", command.folderPath.relative_path)

    command.scrapper.set_starting_page(command.pageNumber)
    while True:
        command.scrapper.download_current_page(command.folderPath)
        hasNext = command.scrapper.set_next_page()
        if not hasNext:
            break

