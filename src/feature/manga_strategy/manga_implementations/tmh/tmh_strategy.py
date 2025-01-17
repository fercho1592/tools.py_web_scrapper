from feature_interfaces.web_drivers.enums import CommonAttrs as COMMON_ATTRS
from feature_interfaces.web_drivers.i_web_reader_driver import IWebReaderDriver
from feature_interfaces.strategies.i_manga_strategy import IMangaStrategy, IMangaPage, IMangaIndex
from feature.manga_strategy.manga_implementations._base_strategy import BaseStrategy
from feature.manga_strategy.manga_implementations.tmh.tmh_index import TmhMangaIndex
from feature.manga_strategy.manga_implementations.tmh.tmh_page import TmhMangaPage
import configs.config_manager as config_manager
import configs.dependency_injection as IOT
from tools.custom_decorators import delayed_view_timer

class TmhMangaStrategy(BaseStrategy, IMangaStrategy):
    @staticmethod
    def is_from_domain(url:str) -> bool:
        config = config_manager.read_config()
        return url.startswith(config["tmh_manga_domain"])

    @staticmethod
    def create_strategy(url:str) -> IMangaStrategy:
        return TmhMangaStrategy(url)

    def get_first_page(self, page_number: int) -> IMangaPage:
        dom_element = IOT.GetWebReaderDriver(self.WebPage)
        # Identify if is a page or index
        if self._is_index_page(dom_element) is False:
            self._logger.debug("Creating an object Page for [%s]", self.WebPage)
            return TmhMangaPage(self, dom_element, self.WebPage)

        # create index page
        self._logger.debug("Creating an object Index for [%s]", self.WebPage)
        index_page = TmhMangaIndex(self, dom_element)
        return index_page.get_manga_page_async(page_number)

    @delayed_view_timer
    def get_index_page_async(self, index_page = 0) -> IMangaIndex:
        del index_page
        dom_reader = IOT.GetWebReaderDriver(self.WebPage)
        return TmhMangaIndex(self, dom_reader)

    @delayed_view_timer
    def get_page_from_url_async(self, url: str) -> IMangaPage:
        dom_reader = IOT.GetWebReaderDriver(url)
        return TmhMangaPage(self, dom_reader, url)

    def _is_index_page(self, dom_element:IWebReaderDriver):
        return len(dom_element.get_by_attrs(COMMON_ATTRS.ID, "content-images")) == 0

    def get_index_page(self, url:str | None = None) -> IMangaIndex:
        url = url if url is not None else self.WebPage
        dom_reader = IOT.GetWebReaderDriver(url)

        if self._is_index_page(dom_reader):
            return TmhMangaIndex(self,dom_reader)

        page = TmhMangaPage(self, dom_reader, url)
        return page.get_index_page()
