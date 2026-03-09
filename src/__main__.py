import asyncio
import configs.dependency_injection as IOT
from configs.queue_reader import read_queue
from feature.services.error_handler import ErrorLogFileHandler
from feature.services.file_manager import FileManager
from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature.services.user_feedback_handler import UserFeedbackHandler
from feature_interfaces.enums.settings_enum import FunctionEnum
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from feature_interfaces.models.folders_struct import MangaFoldersStruct

from handler.image_converter_handler import ImageConverterCommand
from handler.manga_downloader_handler import MangaDownloaderCommand
from handler.pdf_creator_handler import PDFCreatorCommand
from handler.webdav_handler import WebDavCommand

container = IOT.build_container()
_logger: LoggerProtocol = container.resolve_factory(LoggerProtocol, __name__)


async def main():
    fn_image_converte_hangler = container.resolve_function(FunctionEnum.IMAGE_CONVERTER)
    fn_manga_downloader_handler = container.resolve_function(
        FunctionEnum.MANGA_DOWNLOADER
    )
    fn_pdf_creator_handler = container.resolve_function(FunctionEnum.PDF_CREATOR)
    fn_webdav_handler = container.resolve_function(FunctionEnum.WEBDAV)

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
            uiHandler.ShowMessage("PDF already exists")
            await fn_webdav_handler(
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
            await fn_manga_downloader_handler(
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
            uiHandler.ShowMessage("End Manga Download")
            _logger.info("End manga download for [%s]", item.MangaUrl)

        try:
            uiHandler.ShowMessage("Starting image convertion")
            await fn_image_converte_hangler.handle(
                ImageConverterCommand(
                    image_folder=mangaFolder.download_folder,
                    pdf_folder=mangaFolder.converted_folder,
                )
            )
        except Exception as ex:
            del ex
            _logger.error("Error converting images")
            continue
        else:
            fileManager.DeleteAll(mangaFolder.download_folder)

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

            uiHandler.ShowMessage(
                f"PDf created in [{mangaFolder.pdf_folder.get_file_path(item.PdfName)}]"
            )
        except Exception as ex:
            uiHandler.ShowMessageError("Erron on PDF convertion")
            errorHandler.SaveMessageError("Error on PDF conversion", ex)
        else:
            uiHandler.ShowMessage("Deleting Convert Folder")
            fileManager.DeleteAll(mangaFolder.converted_folder)

        try:
            uiHandler.ShowMessage("Uploading PDF to Webdav Service")
            await fn_webdav_handler(
                WebDavCommand(
                    manga_name=item.PdfName,
                    pdf_path=mangaFolder.pdf_folder,
                    dav_path=mangaFolder.dav_folder,
                )
            )
        except Exception as ex:
            _logger.error("Error uploading file to WebDAV: %s", ex)
            continue
        else:
            uiHandler.ShowMessage("Deleting PDF Folder")
            fileManager.DeleteAll(mangaFolder.pdf_folder)

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
