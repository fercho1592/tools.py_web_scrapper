import configs.dependency_injection as IOT
from configs.queue_reader import read_queue, QueueItem
from feature.services.file_manager import DOWNLOAD_FOLDER
from feature.image_converter.image_converter_interfaces import IImageEditorService
from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from feature_interfaces.services.error_handler import IErrorHandler
from feature_interfaces.services.user_feedback_handler import IUserFeedbackHandler
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy
from feature_interfaces.services.file_manager import IFileScrapperManager
from infrastructure.pdf_generator import PdfCreator
from tools.string_path_fix import FixStringsTools

container = IOT.build_container()
_logger: LoggerProtocol = container.resolve_factory(LoggerProtocol, __name__)
image_converter: IImageEditorService = container.resolve(IImageEditorService)
PROSSESING_FOLDER = f"{DOWNLOAD_FOLDER}/../Processing"
PROCESSED_IMAGES = f"{PROSSESING_FOLDER}/converted_images"


def main():
    for item in read_queue():
        print("*************************************************")
        _logger.info("Start process for [%s | %s]", item.FolderName, item.MangaUrl)

        downloadFolder: IFileScrapperManager = container.resolve_factory(IFileScrapperManager, PROSSESING_FOLDER, item.FolderName)
        errorHandler: IErrorHandler = container.resolve_factory(IErrorHandler, item.MangaUrl, downloadFolder)
        uiHandler: IUserFeedbackHandler = container.resolve_factory(IUserFeedbackHandler, item.FolderName, errorHandler)
        strategy:IMangaStrategy = container.resolve_factory(IMangaStrategy, item.MangaUrl)
        scrapper:MangaScraper = container.resolve_factory(MangaScraper, strategy, downloadFolder, uiHandler)
        mangaData = scrapper.get_manga_data()

        try:
            run_manga_downloader(scrapper,item)
        except Exception as ex:
            del ex
            _logger.info("Download incomplete for [%s]", item.MangaUrl)
            continue

        try:
            uiHandler.ShowMessage("Creating Pdf")

            imageFolder = IOT.GetFileScrapperManager(PROCESSED_IMAGES, item.FolderName)
            convert_images(downloadFolder, imageFolder)

            create_pdf(imageFolder, item.PdfName, mangaData)
            artistName = FixStringsTools.ConvertString(mangaData["artist"])
            group = FixStringsTools.ConvertString(mangaData["groups"])
            group = group if group is not None and len(group) else ""
            artistName = artistName if artistName is not None else group
            artistName = artistName.replace("|", "-")
            item.FolderName = item.FolderName.format(artistName = artistName)
            resultFolder = IOT.GetFileScrapperManager(DOWNLOAD_FOLDER, f"{item.FolderName}/..")
            resultFolder.DeleteFile(item.PdfName)
            imageFolder.MoveFileTo(item.PdfName, resultFolder)

            uiHandler.ShowMessage(f"PDf created in [{resultFolder.GetFilePath(item.PdfName)}]")

            _logger.info("Clean folder")
            downloadFolder.DeleteAll(False)
            imageFolder.DeleteAll(False)

            uiHandler.ShowMessage("Folder cleaned")
        except Exception as ex:
            uiHandler.ShowMessageError("Erron on PDF convertion", ex)
            continue

    return

def run_manga_downloader(scrapper: MangaScraper, queueItem: QueueItem):

    if queueItem.DownloadFiles is False:
        _logger.info("Ignore Dowload files")
        return

    try:
        _logger.info("Start manga download for [%s]", queueItem.FolderName)
        scrapper.run_manga_download_async(queueItem.PageNumber)
    finally:
        _logger.info("End manga download for [%s]", queueItem.FolderName)

def create_pdf(folder_manager: IFileScrapperManager,pdf_name:str,manga_data:dict[str,str]) -> None:
    try:
        _logger.info("Start create PDF")
        pdf_creator = PdfCreator(folder_manager, image_converter)
        pdf_creator.CreatePdf(pdf_name, manga_data)
    finally:
        _logger.info("End Create Pdf")

def convert_images(folder_manager: IFileScrapperManager, destFolder: IFileScrapperManager) -> IFileScrapperManager:
    try:
        _logger.info("Start Convert Images")
        for image_name in folder_manager.GetImagesInFolder():
            splited_name = image_name.split(".")
            if splited_name[-1].upper() not in ["PNG", "JPG"]:
                image_converter.convert_image(
                    folder_manager,image_name, splited_name[0], destFolder
                )
            else:
                folder_manager.MoveFileTo(image_name, destFolder)
    finally:
        _logger.info("End Convert Images")

if __name__ == "__main__":
    main()
