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


@log_ejecucion
async def handle(logger: LoggerProtocol, command: MangaDownloaderCommand):
    logger.info("Start manga download for [%s]", command.folderPath.relative_path)

    command.scrapper.set_starting_page(command.pageNumber)
    while True:
        command.scrapper.download_current_page(command.folderPath)
        hasNext = command.scrapper.set_next_page()
        if not hasNext:
            break

