from feature_interfaces.strategies.i_manga_strategy import IMangaPage, IMangaIndex
from feature.manga_strategy.manga_implementations._base_strategy import BaseMangaPage
from feature_interfaces.web_drivers.enums import CommonAttrs as COMMON_ATTRS


class EMangaPage(BaseMangaPage, IMangaPage):

    def get_img_url(self) -> tuple[str, dict[str, str]]:
        self._logger.debug("Getting image url from [%s]", self.Url)
        img = self.Reader.query_selector("#img")
        if img is None:
            raise NotImplementedError("Image not found")

        return img.get_attr_value(COMMON_ATTRS.SRC), {}

    def _get_image_name(self) -> str:
        img_details_ele = self.Reader.query_selector("#i2 span")
        if img_details_ele is None:
            raise NotImplementedError("Image details not found")

        details = img_details_ele.get_value()
        det_array: list[str] = details.split("::")

        self.ImageName = det_array[0].strip()
        return self.ImageName

    def get_image_number(self) -> tuple[str, str]:
        span_elements = self.Reader.query_selector_all("#i2 span")
        if len(span_elements) < 2:
            raise NotImplementedError("Page number details not found")

        self.ImageNumber = span_elements[0].get_value().strip()
        return (
            span_elements[0].get_value().strip(),
            span_elements[1].get_value().strip(),
        )

    def get_next_page_async(self) -> "IMangaPage":
        next_page_url = self._get_next_image_url()
        new_page = self.Strategy.get_page_from_url_async(next_page_url)

        return new_page

    def is_last_page(self) -> bool:
        next_page_url = self._get_next_image_url()
        return self.Url == next_page_url

    def _get_next_image_url(self) -> str:
        img = self.Reader.query_selector("#img")
        if img is None or img.Parent is None:
            raise NotImplementedError("Next page anchor not found")
        return img.Parent.get_attr_value(COMMON_ATTRS.HREF)

    def get_manga_name(self) -> str:
        manga_name = self.Reader.query_selector("h1")
        if manga_name is None:
            raise NotImplementedError("Manga name not found")
        return manga_name.get_value()

    def get_index_page(self) -> IMangaIndex:
        index_arrow = self.Reader.query_selector(".sb a")
        if index_arrow is None:
            raise NotImplementedError("Invalid url")
        href = index_arrow.get_attr_value(COMMON_ATTRS.HREF)

        return self.Strategy.get_index_page(href)
