# Includes
from WebReaders.EWebReader import EWebScraper
from Infrastructure.FileDownloader import FileDownloader
import Infrastructure.MyLogger as MyLogger
import urllib
__logger = MyLogger.GetLogger(__name__)

def GetMangaFromIndex(url, mangaName, page= 1):
    __logger.info(f"Start getting manga from index [{mangaName}]")
    folder = FileDownloader(mangaName)
    folder.createFolderIfNotExist()

    webScrapper = EWebScraper(url)
    index = webScrapper.getIndexPageAsync()
    pageCount = index.getMangaPageCount()
    __logger.info(f"Manga [{mangaName}] contains {pageCount}")
    pageHtmlComponent = index.getMangaPageAsync(page)
    errors = RunMangaDownloaderAsync(pageHtmlComponent, folder, mangaName)
    return (mangaName, errors)

def GetMangaFromPage(url, mangaName):
    __logger.info(f"Start getting manga from page [{mangaName}]")
    folder = FileDownloader(mangaName)
    folder.createFolderIfNotExist()

    webScrapper = EWebScraper(url)
    pageHtmlComponent = webScrapper.getPageAsync()
    errors = RunMangaDownloaderAsync(pageHtmlComponent, folder, mangaName)
    return (mangaName, errors)

def RunMangaDownloaderAsync(pageHtmlComponent, folder, mangaName):
    errors = []
    currentPage = pageHtmlComponent
    while True:
        try:
            imageUrl = currentPage.GetImgUrl()
            imageName = currentPage.getImageName()
            imageNumber = currentPage.getImageNumber()

            __logger.info(f"Trying to get page [{mangaName}: {imageNumber}]")
            folder.downloadImage(imageUrl, imageName)
            if currentPage.isLastPage():
                __logger.info(f"Download of [{mangaName}] complete")
                break
            currentPage = currentPage.GetNextPageAsync()
        except Exception as ex:
            errors.append(currentPage.getImageNumber())
            __logger.error(f"Page: {currentPage.getImageNumber()}")
            currentPage = currentPage.GetNextPageAsync()

    return errors