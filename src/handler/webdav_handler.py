from dataclasses import dataclass
from feature.services.file_manager import FileManager
from feature_interfaces.models.folders_struct import FolderPath
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from feature_interfaces.services.webdav_service import WebDAVService


@dataclass
class WebDavCommand:
    manga_name: str
    pdf_path: FolderPath
    dav_path: FolderPath


class WebDavHandler:
    def __init__(
        self,
        loggerFactory: LoggerProtocol,
        webdav: WebDAVService,
    ):
        self._logger = loggerFactory
        self._webdav_service = webdav

    async def handle(self, command: WebDavCommand) -> None:
        # verifiy if file exist
        if not self.check_file_exists_local(command.pdf_path, command.manga_name):
            raise FileNotFoundError(
                f"PDF file '{command.manga_name}' does not exist in local"
            )
        if self.check_file_exist_webdav(command.dav_path, command.manga_name):
            self._logger.info(f"File '{command.manga_name}' already exists in WebDAV")
            return

        self._webdav_service.upload_file(
            command.pdf_path, command.manga_name, command.dav_path
        )
        pass

    def check_file_exists_local(self, pdf_path: FolderPath, pdfName: str) -> bool:
        fileManager = FileManager(self._logger)
        return fileManager.HasFile(pdf_path, pdfName)

    def check_file_exist_webdav(self, dav_path: FolderPath, pdfName: str) -> bool:
        return self._webdav_service.check_file_exists(dav_path.get_file_path(pdfName))
