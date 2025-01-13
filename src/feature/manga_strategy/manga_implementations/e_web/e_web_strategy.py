import configs.config_manager as config_manager
import configs.dependency_injection as IOT
from feature_interfaces.web_drivers.enums import CommonAttrs as COMMON_ATTRS
from feature_interfaces.web_drivers.i_web_reader_driver import IWebReaderDriver
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy, IMangaIndex, IMangaPage
from feature.manga_strategy.manga_implementations.e_web.e_web_index import EMangaIndex
from feature.manga_strategy.manga_implementations.e_web.e_web_page import EMangaPage
from feature.manga_strategy.manga_implementations._base_strategy import BaseStrategy, DefaultViewTimer

class EMangaStrategy(BaseStrategy,IMangaStrategy):
    @staticmethod
    def is_from_domain(url:str) -> bool:
        config = config_manager.read_config()
        return url.startswith(config["e_manga_domain"])

    @staticmethod
    def create_strategy(url:str) -> IMangaStrategy:
        return EMangaStrategy(url)

    def get_first_page(self, page_number: int) -> IMangaPage:
        dom_element = IOT.GetWebReaderDriver(self.WebPage)

        if self._is_index_page(dom_element) is not True:
            self._logger.debug("Creating an object Page for [%s]", self.WebPage)
            return EMangaPage(self, dom_element, self.WebPage)

        # create index page
        self._logger.debug("Creating an object Index for [%s]", self.WebPage)
        index_page = EMangaIndex(self, dom_element)
        return index_page.get_manga_page_async(page_number)

    def get_index_page_async(self, index_page = 0) -> IMangaIndex:
        dom_reader = IOT.GetWebReaderDriver(f"{self.WebPage}?p={index_page}")

        DefaultViewTimer()
        return EMangaIndex(self, dom_reader)

    def get_page_from_url_async(self, url: str) -> IMangaPage:
        dom_reader = IOT.GetWebReaderDriver(url)
        DefaultViewTimer()
        return EMangaPage(self, dom_reader, url)

    def _is_index_page(self, dom_element: IWebReaderDriver) -> bool:
        return len(dom_element.get_by_attrs(COMMON_ATTRS.ID, "gn")) != 0

    def get_index_page(self, url:str) -> IMangaIndex:
        url = url if url is not None else self.WebPage
        dom_reader = IOT.GetWebReaderDriver(url)

        if self._is_index_page(dom_reader):
            return EMangaIndex(self, dom_reader)

        page = EMangaPage(self, dom_reader, url)
        return page.get_index_page()
