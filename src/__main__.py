'''Main code'''
from infrastructure.file_manager import FileDownloader
from infrastructure.pdf_generator import PdfCreator
from configs.queue_reader import read_queue
from configs.my_logger import get_logger
from feature.manga_strategy.manga_factory import MangaFactory
from feature.manga_strategy.manga_scrapper_context import MangaScraper
from feature.image_converter.pillow_image_converter import PillowImageConverter
from feature.image_converter.image_converter_interfaces import IImageEditorService

_logger = get_logger(__name__)
image_converter: IImageEditorService = PillowImageConverter()

def main():
    for item in read_queue():
        manga_url = item[0].strip()
        folder_name = item[1]
        page_number = item[2]
        pdf_name = item[3]\
          if item[3] is not None\
          else f"{item[1].split("/")[-1]}.pdf"
        pdf_only = item[4]
        print("*************************************************")
        _logger.info("Start process for [%s | %s]", folder_name, manga_url)

        folder_manager = FileDownloader(folder_name)
        folder_manager.create_folder_if_not_exist()

        strategy = MangaFactory.get_manga_strategy(manga_url)
        scrapper = MangaScraper(strategy)
        errors = {}

        if pdf_only is False:
            errors = run_manga_downloader(
              scrapper,
              folder_manager,
              folder_name,
              manga_url,
              page_number)
            if len(errors) != 0:
                _logger.info("Download incomplete for [%s]", manga_url)
                continue

        if pdf_name is not None:
            manga_data = scrapper.get_manga_data()
            converted_folder = convert_images(folder_manager)
            create_pdf(converted_folder, pdf_name, manga_data)
            _logger.info("Cleaning conver folders")
            converted_folder.copy_image_to(
              pdf_name, f"{folder_manager.folder_path}/..")
            converted_folder.delete_all()

    return

def run_manga_downloader(
    scrapper: MangaScraper,
    folder_manager: FileDownloader,
    folder_name: str,
    url: str,
    page_number:int) -> dict[str, str]:

    _logger.info("Start manga download for [%s]", folder_name)
    error_by_manga = scrapper.run_manga_download_async(
      folder_manager, page_number)

    if len(error_by_manga) > 0:
        print(f"Error in these images from [{url}]", error_by_manga)

    _logger.info("End manga download for [%s]", folder_name)
    return error_by_manga

def create_pdf(
    folder_manager: FileDownloader,
    pdf_name:str,
    manga_data:dict[str,str]
  ) -> None:
    _logger.info("Start create PDF")
    pdf_creator = PdfCreator(folder_manager, pdf_name, image_converter)
    pdf_creator.create_pdf(manga_data)
    _logger.info("End Create Pdf")
    return

def convert_images(folder_manager: FileDownloader) -> FileDownloader:
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
    return FileDownloader(full_dest_path)

if __name__ == "__main__":
    main()
