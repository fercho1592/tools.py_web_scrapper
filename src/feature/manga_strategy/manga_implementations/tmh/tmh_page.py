from feature_interfaces.strategies.i_manga_strategy import IMangaPage, IMangaIndex
from feature.manga_strategy.manga_implementations._base_strategy import BaseMangaPage
from feature_interfaces.web_drivers.enums import CommonAttrs as COMMON_ATTRS
from feature_interfaces.web_drivers.enums import CommonTags as COMMON_TAGS

class TmhMangaPage(BaseMangaPage,IMangaPage):

    def get_img_url(self) -> tuple[str, dict[str,str]]:
        image_eles = self.Reader.get_by_tag_name(COMMON_TAGS.IMG,
        COMMON_ATTRS.CLASS, "content-image lazy")
        if len(image_eles) == 0:
            raise NotImplementedError("Image not found")
        url = image_eles[0].get_attr_value(COMMON_ATTRS.DATA_ORIGINAL)
        return url, { "referer": self.Url }

    def _get_image_name(self) -> str:
        image_eles = self.Reader.get_by_attrs(
        COMMON_ATTRS.CLASS, "content-image lazy")
        if len(image_eles) == 0:
            raise NotImplementedError("Image not found")
        image_name = image_eles[0].get_attr_value(COMMON_ATTRS.DATA_ORIGINAL)
        return image_name.split("/")[-1]

    def get_image_number(self) -> tuple[str,str]:
        page_selector = self.Reader.get_by_attrs(COMMON_ATTRS.ID, "select-page")[0]
        selected = page_selector.get_children_by_tag(
            COMMON_TAGS.OPTION, COMMON_ATTRS.SELECTED, "selected")[0]
        last_page = page_selector.get_children_by_tag(
            COMMON_TAGS.OPTION)[-1]
        return (selected.get_value(), last_page.get_value())

    def get_next_page_async(self) -> "IMangaPage":
        image_eles = self.Reader.get_by_tag_name(COMMON_TAGS.I,
        COMMON_ATTRS.CLASS, "fa fa-chevron-right fa-2x")
        if len(image_eles) == 0:
            raise NotImplementedError("Image not found")
        url = image_eles[0].Parent.get_attr_value(COMMON_ATTRS.HREF)
        return self.Strategy.get_page_from_url_async(url)

    def is_last_page(self) -> bool:
        image_eles = self.Reader.get_by_tag_name(COMMON_TAGS.I,
        COMMON_ATTRS.CLASS, "fa fa-chevron-right fa-2x")
        return len(image_eles) == 0

    def get_manga_name(self) -> str:
        header_name = self.Reader.get_by_attrs(
        COMMON_ATTRS.CLASS, "reader-title")[0]
        return header_name.get_value()

    def get_index_page(self) -> IMangaIndex:
        manga_arrows = self.Reader.get_by_attrs(
        COMMON_ATTRS.CLASS, "fa fa-chevron-left")
        index_arrow = manga_arrows[0].Parent
        href = index_arrow.get_attr_value(COMMON_ATTRS.HREF)

        return self.Strategy.get_index_page(href)
