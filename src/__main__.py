import configs.dependency_injection as IOT
from configs.queue_reader import read_queue, QueueItem
from feature.services.error_handler import ErrorLogFileHandler
from feature.services.file_manager import FileManager
from feature.image_converter.image_converter_interfaces import IImageEditorService
from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature.services.user_feedback_handler import UserFeedbackHandler
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from feature_interfaces.models.folders_struct import FolderPath, MangaFoldersStruct
from feature_interfaces.services.webdav_service import WebDAVService
from infrastructure.pdf_generator import PdfCreator

container = IOT.build_container()
_logger: LoggerProtocol = container.resolve_factory(LoggerProtocol, __name__)
image_converter: IImageEditorService = container.resolve(IImageEditorService)
webdav_service: WebDAVService = container.resolve(WebDAVService)


def main():
    for item in read_queue():
        print("*************************************************")
        _logger.info("Start process for [%s | %s]", item.FolderName, item.MangaUrl)

        mangaFolder = MangaFoldersStruct(item.FolderName)
        errorHandler = ErrorLogFileHandler(item.MangaUrl, mangaFolder.error_log_folder)
        uiHandler = UserFeedbackHandler()
        scrapper: MangaScraper = container.resolve_factory(MangaScraper, item.MangaUrl)
        mangaData = scrapper.get_manga_data()

        if check_existing_pdf(mangaFolder, item.PdfName):
            uiHandler.ShowMessage(f"PDF already exists")
            _logger.info("PDF already exists for [%s]", item.MangaUrl)
            if webdav_service.check_file_exists(
                mangaFolder.dav_folder.get_file_path(item.PdfName)
            ):
                continue
            webdav_service.upload_file(
                mangaFolder.pdf_folder, item.PdfName, mangaFolder.dav_folder
            )
            continue

        try:
            uiHandler.ShowMessage(
                f"Start download of {item.MangaUrl} in [{item.FolderName}]"
            )
            run_manga_downloader(scrapper, item, mangaFolder.download_folder)
        except Exception as ex:
            _logger.error("Download incomplete for [%s]", item.MangaUrl)
            errorHandler.SaveDownloadError("Error during manga download", ex)
            continue
        else:
            _logger.info("End manga download for [%s]", item.MangaUrl)

        try:
            convert_images(mangaFolder.download_folder, mangaFolder.converted_folder)
        except Exception as ex:
            del ex
            _logger.error("Error converting images")
            continue

        try:
            uiHandler.ShowMessage("Creating Pdf")

            create_pdf(
                mangaFolder.converted_folder,
                mangaFolder.pdf_folder,
                item.PdfName,
                mangaData,
            )

            # artistName = FixStringsTools.ConvertString(mangaData["artist"])
            # group = FixStringsTools.ConvertString(mangaData["groups"])
            # group = group if group is not None and len(group) else ""
            # artistName = artistName if artistName is not None else group
            # artistName = artistName.replace("|", "-")
            # item.FolderName = item.FolderName.format(artistName = artistName)

            uiHandler.ShowMessage(
                f"PDf created in [{mangaFolder.pdf_folder.get_file_path(item.PdfName)}]"
            )
        except Exception as ex:
            uiHandler.ShowMessageError("Erron on PDF convertion")
            errorHandler.SaveMessageError("Error on PDF conversion", ex)

        try:
            fileManager = FileManager(_logger)
            fileManager.DeleteAll(mangaFolder.download_folder)
            fileManager.DeleteAll(mangaFolder.converted_folder)
        except Exception as ex:
            del ex
            _logger.error("Error deleting temp folders")

        try:
            webdav_service.upload_file(
                mangaFolder.pdf_folder, item.PdfName, mangaFolder.dav_folder
            )
        except Exception as ex:
            _logger.error("Error uploading file to WebDAV: %s", ex)

        _logger.info("End process for [%s | %s]", item.FolderName, item.MangaUrl)
        print("*************************************************")
    return


def check_existing_pdf(pdfFolder: MangaFoldersStruct, pdfName: str) -> bool:
    fileManager = FileManager(_logger)
    if fileManager.HasFile(pdfFolder.pdf_folder, pdfName):
        return True
    if webdav_service.check_file_exists(pdfFolder.dav_folder.get_file_path(pdfName)):
        return True
    return False


def run_manga_downloader(
    scrapper: MangaScraper, queueItem: QueueItem, downloadFolder: FolderPath
) -> None:
    if queueItem.DownloadFiles is False:
        _logger.info("Ignore Dowload files")
        return
    try:
        _logger.info("Start manga download for [%s]", queueItem.FolderName)
        scrapper.set_starting_page(queueItem.PageNumber)
        while True:
            scrapper.download_current_page(downloadFolder)
            hasNext = scrapper.set_next_page()
            if not hasNext:
                break
    except Exception as ex:
        (current_page, total_pages) = scrapper.get_current_page()
        raise Exception(
            f"Error during manga download in item [{current_page}/{total_pages}]"
        ) from ex


def convert_images(initFolder: FolderPath, destFolder: FolderPath) -> None:
    fileManager = FileManager(_logger)
    fileManager.CreateIfNotexist(destFolder)
    try:
        _logger.info("Start Convert Images")
        for image_name in fileManager.GetImagesInFolder(initFolder):
            splited_name = image_name.split(".")
            if splited_name[-1].upper() not in ["PNG", "JPG"]:
                image_converter.convert_image(
                    initFolder, image_name, splited_name[0], destFolder
                )
            else:
                fileManager.MoveFileTo(initFolder, image_name, destFolder)

        fileManager.DeleteAll(initFolder)
    finally:
        _logger.info("End Convert Images")


def create_pdf(
    image_folder: FolderPath,
    pdf_folder: FolderPath,
    pdf_name: str,
    manga_data: dict[str, str],
) -> None:
    try:
        _logger.info("Start create PDF")
        pdf_creator = PdfCreator(image_converter, _logger)
        pdf_creator.CreatePdf(pdf_name, manga_data, image_folder, pdf_folder)
    finally:
        _logger.info("End Create Pdf")


if __name__ == "__main__":
    main()
