'''Main code'''
from infrastructure.file_manager import FileManager
from infrastructure.pdf_generator import PdfCreator
from configs.queue_reader import read_queue, QueueItem
from configs.my_logger import get_logger
from feature.manga_strategy.manga_factory import MangaFactory
from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature.image_converter.pillow_image_converter import PillowImageConverter
from feature.image_converter.image_converter_interfaces import IImageEditorService

_logger = get_logger(__name__)
image_converter: IImageEditorService = PillowImageConverter()

def main():
    for item in read_queue():
        print("*************************************************")
        _logger.info("Start process for [%s | %s]", item.folder_name, item.manga_url)

        folder_manager = FileManager(item.folder_name)
        folder_manager.create_folder_if_not_exist()

        strategy = MangaFactory.get_manga_strategy(item.manga_url)
        scrapper = MangaScraper(strategy)

        try:
            run_manga_downloader(scrapper,folder_manager,item)
        except:
            _logger.info("Download incomplete for [%s]", item.manga_url)
            continue

        if item.pdf_name is not None:
            try:
                print("Creating pdf")
                manga_data = scrapper.get_manga_data()
                converted_folder = convert_images(folder_manager)
                create_pdf(converted_folder, item.pdf_name, manga_data)
                _logger.info("Cleaning conver folders")
                converted_folder.copy_image_to(
                item.pdf_name, f"{folder_manager.folder_path}/..")
                print(f"PDf created in [{folder_manager.folder_path}/{item.pdf_name}]")
                converted_folder.delete_all()
                folder_manager.delete_all()
                print("Folder cleaned")
            except Exception as ex:
                del ex
                folder_manager.write_file("errors.txt",[f"{item.manga_url} | {item.folder_name}",\
                                             "Erron on PDF convertion"])
                continue

    return

def run_manga_downloader(scrapper: MangaScraper,folder_manager: FileManager,queueItem: QueueItem):
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
    manga_data:dict[str,str]
  ) -> None:
    _logger.info("Start create PDF")
    pdf_creator = PdfCreator(folder_manager, pdf_name, image_converter)
    pdf_creator.create_pdf(manga_data)
    _logger.info("End Create Pdf")
    return

def convert_images(folder_manager: FileManager) -> FileManager:
    _logger.info("Start Convert Images")
    dest_folder = "converted_images"
    full_dest_path = f"{folder_manager.folder_path}/{dest_folder}"
    for image_name in folder_manager.get_images_in_folder():
        splited_name = image_name.split(".")
        if splited_name[-1].upper() not in ["PNG", "JPG"]:
            image_converter.convert_image(
                folder_manager,
                image_name,
                splited_name[0],
                dest_folder
            )
        else:
            folder_manager.copy_image_to(image_name, full_dest_path)

    _logger.info("End Convert Images")
    return FileManager(full_dest_path)

if __name__ == "__main__":
    main()
