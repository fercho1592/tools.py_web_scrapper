from configs.queue_reader import QueueItem
from configs.logger_factory import LoggerFactory
from feature_interfaces.protocols.factory_protocol import MangaFactoryProtocol

class MangaDownloaderHandler:
    def __init__(self, loggerFactory: LoggerFactory,factory: MangaFactoryProtocol):
        self._factory = factory
        self._logger = loggerFactory.get_logger(__name__)

    async def download_manga(self, item: QueueItem):
        print("*************************************************")
        self._logger.info("Start process for [%s | %s]", item.FolderName, item.MangaUrl)
        strategy = self._factory.get_manga_strategy(item.MangaUrl)

        downloadFolder = IOT.GetFileScrapperManager(PROSSESING_FOLDER, item.FolderName)
        errorHandler = IOT.GetErrorHandler(item.MangaUrl, downloadFolder)
        uiHandler = IOT.GetUserFeddbackHandler(item.FolderName, errorHandler)
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
