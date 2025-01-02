import configs.dependency_injection as IOT
from configs.queue_reader import read_queue, QueueItem
from configs.my_logger import get_logger
from infrastructure.pdf_generator import PdfCreator
from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature.services.file_manager import FileManager, DOWNLOAD_FOLDER

_logger = get_logger(__name__)
image_converter = IOT.GetImageConverter()
DEST_FOLDER = "converted_images"
PROSSESING_FOLDER = "../Processing"


def main():
    for item in read_queue():
        print("*************************************************")
        _logger.info("Start process for [%s | %s]", item.folder_name, item.manga_url)

        resultFolder = f"{DOWNLOAD_FOLDER}/{item.folder_name}"
        processingFolder = f"{DOWNLOAD_FOLDER}/{PROSSESING_FOLDER}/{item.folder_name}"
        uiHandler = IOT.GetUserFeddbackHandler(item.folder_name, errorHandler)
        folderManager = IOT.GetFileManager(DOWNLOAD_FOLDER, processingFolder)
        errorHandler = IOT.GetErrorHandler(item.manga_url, folderManager)
        scrapper = IOT.GetMangaScrapper(IOT.GetMangaStrategy(item.manga_url), uiHandler)
        mangaData = scrapper.get_manga_data()

        try:
            run_manga_downloader(scrapper,folderManager,item)
        except:
            _logger.info("Download incomplete for [%s]", item.manga_url)
            continue

        try:
            uiHandler.ShowMessage("Creating Pdf")
            _logger.info("Converting images")
            converted_folder = convert_images(folderManager)
            _logger.info("Creating PDF")
            create_pdf(converted_folder, item.pdf_name, mangaData)
            _logger.info("Cleaning conver folders")
            converted_folder.MoveFileTo(item.pdf_name, resultFolder)
            uiHandler.ShowMessage(f"PDf created in [{resultFolder}/{item.pdf_name}]")
            _logger.info("Clean folder")
            converted_folder.DeleteAll()
            folderManager.DeleteAll()
            uiHandler.ShowMessage("Folder cleaned")
        except Exception as ex:
            del ex
            folderManager.write_file("errors.txt",[f"{item.manga_url} | {item.folder_name}",\
                                            "Erron on PDF convertion"])
            continue

    return

def run_manga_downloader(
        scrapper: MangaScraper,
        folder_manager: FileManager,
        queueItem: QueueItem):
    
    if queueItem.download_files is False:
        _logger.info("Ignore Dowload files")
        return

    try:
        _logger.info("Start manga download for [%s]", queueItem.folder_name)
        scrapper.run_manga_download_async(folder_manager, queueItem.page_number)
    finally:
        _logger.info("End manga download for [%s]", queueItem.folder_name)

def create_pdf(
        folder_manager: FileManager,
        pdf_name:str,
        manga_data:dict[str,str]) -> None:
    try:
        _logger.info("Start create PDF")
        pdf_creator = PdfCreator(folder_manager, pdf_name, image_converter)
        pdf_creator.create_pdf(manga_data)
    finally:
        _logger.info("End Create Pdf")

def convert_images(folder_manager: FileManager) -> FileManager:
    try:
        _logger.info("Start Convert Images")
        full_dest_path = f"{folder_manager.GetFolderPath()}/{DEST_FOLDER}"
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
                folder_manager.MoveFileTo(image_name, full_dest_path)

        return IOT.GetFileManager(folder_manager.GetFolderPath(), DEST_FOLDER)
    finally:
        _logger.info("End Convert Images")

if __name__ == "__main__":
    main()
