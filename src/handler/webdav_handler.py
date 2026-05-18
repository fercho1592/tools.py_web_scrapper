from dataclasses import dataclass
from feature.services.file_manager import FileManager
from feature_interfaces.models.folders_struct import FolderPath
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from feature_interfaces.services.webdav_service import WebDAVService
from wrappers.handler_decorators import log_ejecucion


@dataclass
class WebDavCommand:
    manga_name: str
    pdf_path: FolderPath
    dav_path: FolderPath


@log_ejecucion
def handle(
    webdav_service: WebDAVService,
    fileManager: FileManager,
    logger: LoggerProtocol,
    command: WebDavCommand,
) -> None:
    # verifiy if file exist
    if not check_file_exists_local(fileManager, command.pdf_path, command.manga_name):
        raise FileNotFoundError(
            f"PDF file '{command.manga_name}' does not exist in local"
        )
    if check_file_exist_webdav(webdav_service, command.dav_path, command.manga_name):
        logger.info(f"File '{command.manga_name}' already exists in WebDAV")
        return

    webdav_service.upload_file(command.pdf_path, command.manga_name, command.dav_path)
    pass


def check_file_exists_local(
    fileManager: FileManager, pdf_path: FolderPath, pdfName: str
) -> bool:
    return fileManager.HasFile(pdf_path, pdfName)


def check_file_exist_webdav(
    webdav_service: WebDAVService, dav_path: FolderPath, pdfName: str
) -> bool:
    return webdav_service.check_file_exists(dav_path.get_file_path(pdfName))
