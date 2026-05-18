from dataclasses import dataclass
from typing import Protocol
from feature_interfaces.models.folders_struct import VideoFoldersStruct
from feature_interfaces.protocols.config_protocol import LoggerProtocol

class VideoDownloaderProtocol(Protocol):
    """Protocol for video downloading service"""
    def download(self, url: str, output_path: str) -> None:
        """Download video from URL to specified path"""
        ...


@dataclass
class VideoDownloaderCommand:
    url: str
    video_name: str
    folderStruct: VideoFoldersStruct


class VideoDownloaderHandler:
    def __init__(self, logger_factory: LoggerProtocol, downloader: VideoDownloaderProtocol):
        self._logger = logger_factory
        self._downloader = downloader

    async def handle(self, command: VideoDownloaderCommand):
        try:
            self._logger.info(
                "Start video download for [%s]", command.video_name
            )

            output_path = command.folderStruct.download_folder.get_file_path(
                command.video_name
            )
            self._downloader.download(command.url, output_path)

            self._logger.info(
                "Video download completed successfully [%s]", command.video_name
            )
        except Exception as ex:
            self._logger.error(
                "Error during video download [%s]: %s", command.video_name, str(ex)
            )
            raise Exception(
                f"Error during video download for [{command.video_name}]"
            ) from ex