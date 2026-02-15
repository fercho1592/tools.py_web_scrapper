import asyncio
import configs.dependency_injection as IOT
from configs.queue_reader import QueueItem, read_queue
from feature.services.error_handler import ErrorLogFileHandler
from feature.services.file_manager import FileManager
from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature.services.user_feedback_handler import UserFeedbackHandler
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from feature_interfaces.models.folders_struct import MangaFoldersStruct
from handler.image_converter_handler import ImageConverterHandler, ImageConverterCommand
from handler.manga_downloader_handler import (
    MangaDownloaderHandler,
    MangaDownloaderCommand,
)
from handler.pdf_creator_handler import PDFCreatorHandler, PDFCreatorCommand
from handler.webdav_handler import WebDavHandler, WebDavCommand

container = IOT.build_container()
_logger: LoggerProtocol = container.resolve_factory(LoggerProtocol, __name__)
image_converte_hangler: ImageConverterHandler = container.resolve(ImageConverterHandler)
manga_downloader_handler: MangaDownloaderHandler = container.resolve(
    MangaDownloaderHandler
)
pdf_creator_handler: PDFCreatorHandler = container.resolve(PDFCreatorHandler)
webdav_handler: WebDavHandler = container.resolve(WebDavHandler)


async def main():
    for item in read_queue():
        print("*************************************************")
        _logger.info("Start process for [%s | %s]", item.FolderName, item.MangaUrl)

        mangaFolder = MangaFoldersStruct(item.FolderName)
        errorHandler = ErrorLogFileHandler(item.MangaUrl, mangaFolder.error_log_folder)
        uiHandler = UserFeedbackHandler()
        scrapper: MangaScraper = container.resolve_factory(MangaScraper, item.MangaUrl)
        mangaData = scrapper.get_manga_data()
        fileManager = FileManager(_logger)

        if check_existing_pdf(mangaFolder, item.PdfName):
            uiHandler.ShowMessage(f"PDF already exists")
            await webdav_handler.handle(
                WebDavCommand(
                    manga_name=item.PdfName,
                    pdf_path=mangaFolder.pdf_folder,
                    dav_path=mangaFolder.dav_folder,
                )
            )

            continue

        try:
            uiHandler.ShowMessage(
                f"Start download of {item.MangaUrl} in [{item.FolderName}]"
            )
            await manga_downloader_handler.handle(
                MangaDownloaderCommand(
                    scrapper=scrapper,
                    pageNumber=0,
                    folderPath=mangaFolder.download_folder,
                )
            )

        except Exception as ex:
            _logger.error("Download incomplete for [%s]", item.MangaUrl)
            errorHandler.SaveDownloadError("Error during manga download", ex)
            continue
        else:
            _logger.info("End manga download for [%s]", item.MangaUrl)

        try:
            await image_converte_hangler.handle(
                ImageConverterCommand(
                    image_folder=mangaFolder.download_folder,
                    pdf_folder=mangaFolder.converted_folder,
                )
            )
            #fileManager.DeleteAll(mangaFolder.download_folder)
        except Exception as ex:
            del ex
            _logger.error("Error converting images")
            continue

        try:
            uiHandler.ShowMessage("Creating Pdf")

            await pdf_creator_handler.handle(
                PDFCreatorCommand(
                    image_folder=mangaFolder.converted_folder,
                    pdf_folder=mangaFolder.pdf_folder,
                    pdf_name=item.PdfName,
                    manga_data=mangaData,
                )
            )

            uiHandler.ShowMessage(
                f"PDf created in [{mangaFolder.pdf_folder.get_file_path(item.PdfName)}]"
            )
        except Exception as ex:
            uiHandler.ShowMessageError("Erron on PDF convertion")
            errorHandler.SaveMessageError("Error on PDF conversion", ex)

        try:
            # fileManager.DeleteAll(mangaFolder.download_folder)
            # fileManager.DeleteAll(mangaFolder.converted_folder)
            ...
        except Exception as ex:
            del ex
            _logger.error("Error deleting temp folders")
            continue

        try:
            await webdav_handler.handle(
                WebDavCommand(
                    manga_name=item.PdfName,
                    pdf_path=mangaFolder.pdf_folder,
                    dav_path=mangaFolder.dav_folder,
                )
            )

        except Exception as ex:
            _logger.error("Error uploading file to WebDAV: %s", ex)
            continue

        _logger.info("End process for [%s | %s]", item.FolderName, item.MangaUrl)
        print("*************************************************")
    return


def check_existing_pdf(pdfFolder: MangaFoldersStruct, pdfName: str) -> bool:
    fileManager = FileManager(_logger)
    if fileManager.HasFile(pdfFolder.pdf_folder, pdfName):
        return True
    return False


if __name__ == "__main__":
    asyncio.run(main())
