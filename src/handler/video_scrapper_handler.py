from dataclasses import dataclass
from typing import Protocol
from feature_interfaces.models.folders_struct import VideoFoldersStruct
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from feature_interfaces.web_drivers.i_web_reader_driver import IWebReaderDriver
from feature_interfaces.web_drivers.enums import CommonTags, CommonAttrs


class VideoScrapperProtocol(Protocol):
    """Protocol for web scrapping service"""

    def get_driver(self, url: str) -> IWebReaderDriver:
        """Get web driver for URL"""
        ...


@dataclass
class VideoSource:
    video_url: str
    video_name: str


@dataclass
class VideoScrapperCommand:
    page_url: str
    folderStruct: VideoFoldersStruct
    scrapper_type: str  # 'single' for single video, 'series' for multiple pages


class VideoScrapperHandler:
    def __init__(self, logger_factory: LoggerProtocol, scrapper: VideoScrapperProtocol):
        self._logger = logger_factory
        self._scrapper = scrapper

    async def handle(self, command: VideoScrapperCommand) -> list[VideoSource]:
        try:
            self._logger.info("Start video scrapping for [%s]", command.page_url)

            driver = self._scrapper.get_driver(command.page_url)
            video_sources = self._extract_video_sources(driver, command.scrapper_type)

            self._logger.info(
                "Video scrapping completed successfully [%s] - Found %d videos",
                command.page_url,
                len(video_sources),
            )
            return video_sources

        except Exception as ex:
            self._logger.error(
                "Error during video scrapping [%s]: %s", command.page_url, str(ex)
            )
            raise Exception(
                f"Error during video scrapping for [{command.page_url}]"
            ) from ex

    def _extract_video_sources(
        self, driver: IWebReaderDriver, scrapper_type: str
    ) -> list[VideoSource]:
        video_sources = []

        if scrapper_type == "single":
            video_sources = self._extract_single_video(driver)
        elif scrapper_type == "series":
            video_sources = self._extract_series_videos(driver)

        return video_sources

    def _extract_single_video(self, driver: IWebReaderDriver) -> list[VideoSource]:
        """Extract single video from page"""
        video_elements = driver.get_by_tag_name(CommonTags.VIDEO)

        sources = []
        for video_elem in video_elements:
            src_elements = video_elem.get_children_by_tag(CommonTags.SOURCE)
            for src in src_elements:
                video_url = src.get_attr_value(CommonAttrs.SRC)
                video_name = src.get_attr_value(CommonAttrs.TITLE) or "video"
                sources.append(VideoSource(video_url=video_url, video_name=video_name))

        return sources

    def _extract_series_videos(self, driver: IWebReaderDriver) -> list[VideoSource]:
        """Extract video links from series pages"""
        link_elements = driver.get_by_tag_name(CommonTags.A)

        sources = []
        for link in link_elements:
            if link.has_attr(CommonAttrs.HREF):
                page_url = link.get_attr_value(CommonAttrs.HREF)
                link_text = link.get_value()
                sources.append(VideoSource(video_url=page_url, video_name=link_text))

        return sources


# NOTES: Additional methods required for IWebReaderDriver implementation:
# 1. navigate(url: str) -> None: Navigate to a specific URL
# 2. wait_for_element(tag: CommonTags, timeout: int) -> IWebElementDriver: Wait for element to load
# 3. execute_script(script: str) -> any: Execute JavaScript on page
# 4. close() -> None: Close/cleanup driver resources