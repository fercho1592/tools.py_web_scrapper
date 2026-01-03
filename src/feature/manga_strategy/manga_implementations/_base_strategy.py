from feature_interfaces.protocols.config_protocol import LoggerProtocol
from feature_interfaces.services.http_service import IHttpService
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy
from feature_interfaces.web_drivers.i_web_reader_driver import IWebReaderDriver
import configs.logger_factory as logger_factory
from abc import ABC


class BaseStrategy(ABC):
    def __init__(self, web_page: str, logger: LoggerProtocol, httpService: IHttpService):
        self._logger = logger
        self.HttpService = httpService
        self.WebPage = web_page

    def get_url(self) -> str:
        return self.WebPage

class BaseMangaIndex(ABC):
    def __init__(self, strategy: IMangaStrategy,dom_reader: IWebReaderDriver, logger: LoggerProtocol) -> None:
        super().__init__()
        self.Strategy = strategy
        self.DomReader = dom_reader
        self._logger = logger

class BaseMangaPage(ABC):
    def __init__(
        self, strategy:IMangaStrategy, dom_reader:IWebReaderDriver, url: str, logger: LoggerProtocol):
        self.Strategy = strategy
        self.Reader = dom_reader
        self.Url:str = url
        self.ImageName:str | None = None
        self.ImageNumber:int | None = None
        self._logger = logger

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
