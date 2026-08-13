from contracts.strategies.i_manga_strategy import IMangaPage, IMangaIndex
from contracts.web_drivers.enums import CommonAttrs as COMMON_ATTRS
from manga.manga_implementations._base_strategy import BaseMangaPage


class TmhMangaPage(BaseMangaPage, IMangaPage):
    def get_img_url(self) -> tuple[str, dict[str, str]]:
        image_ele = self.Reader.query_selector("img.content-image.lazy")
        if image_ele is None:
            raise NotImplementedError("Image not found")
        url = image_ele.get_attr_value(COMMON_ATTRS.DATA_ORIGINAL)
        return url, {"referer": self.Url}

    def _get_image_name(self) -> str:
        image_ele = self.Reader.query_selector("img.content-image.lazy")
        if image_ele is None:
            raise NotImplementedError("Image not found")
        image_name = image_ele.get_attr_value(COMMON_ATTRS.DATA_ORIGINAL)
        return image_name.split("/")[-1]

    def get_image_number(self) -> tuple[str, str]:
        page_selector = self.Reader.query_selector("#select-page")
        if page_selector is None:
            raise NotImplementedError("Page selector not found")

        selected = page_selector.query_selector("option[selected=selected]")
        last_page = page_selector.query_selector_all("option")
        if selected is None or not last_page:
            raise NotImplementedError("Page number details not found")

        return (selected.get_value(), last_page[-1].get_value())

    def get_next_page_async(self) -> "IMangaPage":
        next_icon = self.Reader.query_selector("i.fa.fa-chevron-right.fa-2x")
        if next_icon is None or next_icon.Parent is None:
            raise NotImplementedError("Next page icon not found")
        url = next_icon.Parent.get_attr_value(COMMON_ATTRS.HREF)
        return self.Strategy.get_page_from_url_async(url)

    def is_last_page(self) -> bool:
        next_icon = self.Reader.query_selector("i.fa.fa-chevron-right.fa-2x")
        return next_icon is None

    def get_manga_name(self) -> str:
        header_name = self.Reader.get_by_attrs(COMMON_ATTRS.CLASS, "reader-title")[0]
        return header_name.get_value()

    def get_index_page(self) -> IMangaIndex:
        manga_arrows = self.Reader.get_by_attrs(
            COMMON_ATTRS.CLASS, "fa fa-chevron-left"
        )
        index_arrow = manga_arrows[0].Parent
        href = index_arrow.get_attr_value(COMMON_ATTRS.HREF)
        return self.Strategy.get_index_page(href)
