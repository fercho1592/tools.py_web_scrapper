import asyncio
import core.config.dependency_injection as IOT
from core.config.queue_reader import read_queue
from core.services.error_handler import ErrorLogFileHandler
from core.services.file_manager import FileManager
from manga.manga_scrapper_context import MangaScraper
from core.services.user_feedback_handler import UserFeedbackHandler
from contracts.enums.settings_enum import FunctionEnum
from contracts.protocols.config_protocol import LoggerProtocol
from contracts.models.folders_struct import MangaFoldersStruct

from services.image_converter_service import ImageConverterCommand
from services.manga_downloader_service import MangaDownloaderCommand
from services.pdf_creator_service import PDFCreatorCommand
from services.webdav_service import WebDavCommand

container = IOT.build_container()
_logger: LoggerProtocol = container.resolve_factory(LoggerProtocol, __name__)


async def main():
    fn_image_converte_hangler = container.resolve_function(FunctionEnum.IMAGE_CONVERTER)
    fn_manga_downloader_handler = container.resolve_function(
        FunctionEnum.MANGA_DOWNLOADER
    )
    fn_pdf_creator_handler = container.resolve_function(FunctionEnum.PDF_CREATOR)
    fn_webdav_handler = container.resolve_function(FunctionEnum.WEBDAV)
    uiHandler = UserFeedbackHandler()
    fileManager = FileManager(_logger)

    for item in read_queue():
        print("*************************************************")
        _logger.info("Start process for [%s | %s]", item.FolderName, item.MangaUrl)

        mangaFolder = MangaFoldersStruct(item.FolderName)
        errorHandler = ErrorLogFileHandler(item.MangaUrl, mangaFolder.error_log_folder)
        scrapper: MangaScraper = container.resolve_factory(MangaScraper, item.MangaUrl)
        mangaData = scrapper.get_manga_data()

        # finish_download = await upload_to_webdav(
        #     mangaFolder, item.PdfName, mangaFolder.dav_folder
        # )

        # if finish_download is True:
        #     _logger.info(
        #         "File already exists in WebDAV, skipping download and conversion for [%s]",
        #         item.MangaUrl,
        #     )
        #     continue

        try:
            uiHandler.ShowMessage("Starting image convertion")
            await fn_image_converte_hangler(
                ImageConverterCommand(
                    image_folder=mangaFolder.download_folder,
                    pdf_folder=mangaFolder.converted_folder,
                )
            )

            fileManager.DeleteAll(mangaFolder.download_folder)
        except Exception as ex:
            del ex
            _logger.error("Error converting images")
            continue

        continue

        try:
            uiHandler.ShowMessage("Creating Pdf")

            await fn_pdf_creator_handler(
                PDFCreatorCommand(
                    image_folder=mangaFolder.converted_folder,
                    pdf_folder=mangaFolder.pdf_folder,
                    pdf_name=item.PdfName,
                    manga_data=mangaData,
                )
            )

            uiHandler.ShowMessage("Deleting Convert Folder")
            fileManager.DeleteAll(mangaFolder.converted_folder)

            uiHandler.ShowMessage(
                f"PDf created in [{mangaFolder.pdf_folder.get_file_path(item.PdfName)}]"
            )
        except Exception as ex:
            uiHandler.ShowMessageError("Erron on PDF convertion")
            errorHandler.SaveMessageError("Error on PDF conversion", ex)

        try:
            uiHandler.ShowMessage("Uploading PDF to Webdav Service")
            await upload_to_webdav(mangaFolder, item.PdfName, mangaFolder)
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


async def upload_to_webdav(
    pdfFolder: MangaFoldersStruct, pdfName: str, davFolder: MangaFoldersStruct
):
    fileManager = FileManager(_logger)
    if check_existing_pdf(pdfFolder, pdfName) is False:
        return False
    fn_webdav_handler = container.resolve_function(FunctionEnum.WEBDAV)
    await fn_webdav_handler(
        WebDavCommand(
            manga_name=pdfName,
            pdf_path=pdfFolder.pdf_folder,
            dav_path=davFolder.dav_folder,
        )
    )

    fileManager.DeleteAll(pdfFolder)

    return True


if __name__ == "__main__":
    asyncio.run(main())
