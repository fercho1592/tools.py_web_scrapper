import configs.dependency_injection as IOT
from configs.queue_reader import read_queue, QueueItem
from configs.my_logger import get_logger
from infrastructure.pdf_generator import PdfCreator
from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature.services.file_manager import FileManager, DOWNLOAD_FOLDER
from feature_interfaces.services.file_manager import IFileManager

_logger = get_logger(__name__)
image_converter = IOT.GetImageConverter()
DEST_FOLDER = "converted_images"
PROSSESING_FOLDER = "../Processing"


def main():
    for item in read_queue():
        print("*************************************************")
        _logger.info("Start process for [%s | %s]", item.FolderName, item.MangaUrl)

        imageFolder = f"{DOWNLOAD_FOLDER}/{item.FolderName}"
        resultFolder = f"{DOWNLOAD_FOLDER}/{item.FolderName}/.."
        processingFolder = f"{DOWNLOAD_FOLDER}/{PROSSESING_FOLDER}/{item.FolderName}"
        downloadFolder = IOT.GetFileManager(DOWNLOAD_FOLDER, processingFolder)
        imageFolder = IOT.GetFileManager(DOWNLOAD_FOLDER, imageFolder)
        resultFolder = IOT.GetFileManager(DOWNLOAD_FOLDER, resultFolder)
        errorHandler = IOT.GetErrorHandler(item.MangaUrl, downloadFolder)
        uiHandler = IOT.GetUserFeddbackHandler(item.FolderName, errorHandler)
        strategy = IOT.GetMangaStrategy(item.MangaUrl)
        scrapper = IOT.GetMangaScrapper(strategy, uiHandler, downloadFolder)
        mangaData = scrapper.get_manga_data()

        try:
            run_manga_downloader(scrapper,item)
        except Exception as ex:
            del ex
            _logger.info("Download incomplete for [%s]", item.MangaUrl)
            continue

        try:
            uiHandler.ShowMessage("Creating Pdf")

            convert_images(downloadFolder)
            create_pdf(downloadFolder, item.PdfName, mangaData)
            downloadFolder.MoveFileTo(item.PdfName, resultFolder)

            uiHandler.ShowMessage(f"PDf created in [{resultFolder}/{item.PdfName}]")

            _logger.info("Clean folder")
            downloadFolder.DeleteAll()
            imageFolder.DeleteAll()

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

def create_pdf(folder_manager: FileManager,pdf_name:str,manga_data:dict[str,str]) -> None:
    try:
        _logger.info("Start create PDF")
        pdf_creator = PdfCreator(folder_manager, image_converter)
        pdf_creator.CreatePdf(pdf_name, manga_data)
    finally:
        _logger.info("End Create Pdf")

def convert_images(folder_manager: FileManager) -> IFileManager:
    try:
        _logger.info("Start Convert Images")
        full_dest_path = f"{folder_manager.GetFolderPath()}/{DEST_FOLDER}"
        destFolder = IOT.GetFileManager(DOWNLOAD_FOLDER, full_dest_path)
        for image_name in folder_manager.GetImagesInFolder():
            splited_name = image_name.split(".")
            if splited_name[-1].upper() not in ["PNG", "JPG"]:
                image_converter.convert_image(
                    folder_manager,
                    image_name,
                    splited_name[0],
                    DEST_FOLDER
                )
            else:
                folder_manager.MoveFileTo(image_name, destFolder)

        return destFolder
    finally:
        _logger.info("End Convert Images")

if __name__ == "__main__":
    main()
