from typing import Self
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy, IMangaIndex, IMangaPage
from feature_interfaces.web_drivers.i_web_reader_driver import IWebReaderDriver
import configs.my_logger as my_logger
import configs.dependency_injection as IOT
import time
from abc import ABC

from abc import abstractmethod



def DefaultViewTimer():
    delay_seconds = 5
    time.sleep(delay_seconds)

class BaseStrategy(IMangaStrategy, ABC):
    @staticmethod
    @abstractmethod
    def is_from_domain(url:str) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def create_strategy(url:str) -> IMangaStrategy:
        pass

    def __init__(self, web_page: str):
        self._logger = my_logger.get_logger(__name__)
        self.WebPage = web_page
        self.HttpService = IOT.GetHttpService()

    @abstractmethod
    def get_page_from_url_async(self, url: str) -> IMangaPage:
        pass

    @abstractmethod
    def get_first_page(self, page_number: int = 0) -> IMangaPage:
        pass

    @abstractmethod
    def get_index_page_async(self, index_page = 0) -> IMangaIndex:
        pass

    def get_url(self) -> str:
        return self.WebPage

class BaseMangaIndex(IMangaIndex, ABC):
    def __init__(self, strategy: IMangaStrategy,dom_reader: IWebReaderDriver) -> None:
        super().__init__()
        self.Strategy = strategy
        self.DomReader = dom_reader
        self._logger = my_logger.get_logger(__name__)

    @staticmethod
    @abstractmethod
    def get_max_pages_in_index() -> int:
        pass

    @abstractmethod
    def get_manga_name(self) -> str:
        pass

    @abstractmethod
    def _get_index_page(self, index_page: int) -> Self:
        pass

    @abstractmethod
    def get_manga_page_async(self, page:int = 0) -> IMangaPage:
        pass

class BaseMangaPage(IMangaPage, ABC):
    def __init__(
        self, strategy:IMangaStrategy, dom_reader:IWebReaderDriver, url: str):
        self.Strategy = strategy
        self.Reader = dom_reader
        self.Url:str = url
        self.ImageName:str | None = None
        self.ImageNumber:int | None = None
        self._logger = my_logger.get_logger(__name__)

    @abstractmethod
    def get_img_url(self) -> tuple[str, dict[str, str]]:
        pass

    @abstractmethod
    def _get_image_name(self) -> str:
        pass

    @abstractmethod
    def get_image_number(self) -> tuple[str,str]:
        pass

    @abstractmethod
    def get_manga_name(self) ->str:
        pass

    def get_image_name(self) -> str:
        default_image_name = self._get_image_name()
        (image_number, max_image_count) = self.get_image_number()
        zero_array = ["0" for i in range(len(str(max_image_count))-len(str(image_number)))]
        zero_array.append(image_number)
        zero_array.append("_")
        zero_array.append(default_image_name)
        return "".join(zero_array)

    def get_image_type(self) -> str:
        name = self.get_image_name()
        image_type = name.rsplit(".", maxsplit=-1)[-1]
        return image_type
